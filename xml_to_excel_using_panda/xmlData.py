#!/usr/bin/python
import sys
import re
import zipfile
import pandas as pd
import dateutil.parser
import xml.etree.ElementTree as ETree


class ZipUtil:
    file_list = []
    path = ''

    def __init__(self, path):
        self.path = path

    def get_all_xml_files(self):
        zf = zipfile.ZipFile(self.path, 'r')
        # loop through the filename inside the zip
        for name in zf.namelist():
            if name.endswith('/') or str(name).startswith('__MACOSX/'):
                continue
            if name.endswith('.xml'):
                f = zf.open(name)
                self.file_list.append(f)


class XmlUtil:
    def __init__(self, xmlFileArray):
        self.xmlFileArray = xmlFileArray
        self.fileList = []
        self.allWbtsAndWcel = []
        self.allTypeAndCounters = []

    def parse_xml_file(self):
        for key, file in enumerate(self.xmlFileArray):
            # Get data
            self.read_wdata_params(file, key + 1)

    def get_namespace(self, element):
        m = re.match(r'\{(.*)\}', element.tag)
        return m.group(1) if m else ''

    def remove_namespace(self, doc, namespace):
        # Remove namespace in the passed document in place
        ns = u'{%s}' % namespace
        nsl = len(ns)
        for elem in doc.iter():
            if elem.tag.startswith(ns):
                elem.tag = elem.tag[nsl:]

    def getData(self, pmSetupData):
        # get date and time
        dateTimeStr = pmSetupData.attrib['startTime']
        d = dateutil.parser.parse(dateTimeStr.split("+")[0])
        obj = {'date': d.strftime('%Y-%m-%d'), 'time': d.strftime('%H:%M:%S')}

        # get duration
        obj['duration'] = pmSetupData.attrib['interval']

        return obj

    def readWBTSandWCEL(self, wString):
        wbtsRgx = re.compile(r'WBTS-\d+')
        wbtsGrp = wbtsRgx.search(wString)
        wcelRgx = re.compile(r'WCEL-\d+')
        wcelGrp = wcelRgx.search(wString)
        return {'wbts': wbtsGrp.group(0).split('-')[1], 'wcel': wcelGrp.group(0).split('-')[1]}

    def get_wdata(self, pmResult, fileCount, dataObj):
        for moData in pmResult.iter('MO'):
            for dnData in moData.iter('DN'):
                if 'WBTS' in dnData.text:
                    valObj = self.readWBTSandWCEL(dnData.text)
                    obj = {
                        'File number': fileCount,
                        'Date':  dataObj['date'],
                        'Start Time': dataObj['time'],
                        'Duration': dataObj['duration'],
                        'WBTS': valObj['wbts'],
                        'WCEL': valObj['wcel']
                    }
                    self.allWbtsAndWcel.append(obj)

    def get_type_and_counter(self, pmResult, fileCount):
        for pmTarget in pmResult.iter('PMTarget'):
            for elem in pmTarget:
                obj = {
                    'File Number': fileCount,
                    'Types': pmTarget.attrib['measurementType'],
                    'Counters': elem.tag,
                    'Counters Values': elem.text
                }
                self.allTypeAndCounters.append(obj)

    def parse_data_from_root(self, root, fileCount):
        for pmSetupData in root.iter('PMSetup'):
            dataObj = self.getData(pmSetupData)
            # get WBTS and WCEL
            for pmResult in pmSetupData.iter('PMMOResult'):
                self.get_wdata(pmResult, fileCount, dataObj)
                self.get_type_and_counter(pmResult, fileCount)

    def read_wdata_params(self, file, fileCount):
        obj = {'File Titles': file.name, 'File Number': fileCount}
        self.fileList.append(obj)
        prstree = ETree.parse(file)
        root = prstree.getroot()
        nameSpace = self.get_namespace(root)
        self.remove_namespace(root, nameSpace)
        self.parse_data_from_root(root, fileCount)


class ExcelUtil:
    fileList = None
    wbtsData = None
    typeAndCounterData = None

    fileFrame = None
    info1Frame = None
    info2Frame = None
    writer = None

    def __init__(self, fileList, wbtsData, typeAndCounterData):
        self.fileList = fileList
        self.wbtsData = wbtsData
        self.typeAndCounterData = typeAndCounterData

    def convert_to_data_frames(self):
        self.fileFrame = pd.DataFrame(self.fileList)
        self.info1Frame = pd.DataFrame(self.wbtsData)
        self.info2Frame = pd.DataFrame(self.typeAndCounterData)

    def coulmnWidthAuto(self, frame, sheet):
        # Auto-adjust columns' width
        for column in frame:
            column_width = max(frame[column].astype(
                str).map(len).max(), len(column))
            col_idx = frame.columns.get_loc(column)
            self.writer.sheets[sheet].set_column(
                col_idx, col_idx, column_width)

    def generate_excel(self, output_file_path):
        self.writer = pd.ExcelWriter(output_file_path)
        self.fileFrame.to_excel(self.writer, sheet_name='FILES', index=False)
        self.coulmnWidthAuto(self.fileFrame, 'FILES')
        self.info1Frame.to_excel(self.writer, sheet_name='INFO1', index=False)
        self.coulmnWidthAuto(self.info1Frame, 'INFO1')
        self.info2Frame.to_excel(self.writer, sheet_name='INFO2', index=False)
        self.coulmnWidthAuto(self.info2Frame, 'INFO2')
        self.writer.save()


def main():
    if not len(sys.argv) > 2:
        print(
            'Error : Zip file location needed like "python xmlData.py \'Archive_bak.zip\' \'Result.xlsx\'" ')
        exit()

    print("################### Genrating Excel File ###################")
    zipPath = sys.argv[1]
    outPutPath = sys.argv[2]
    zipObj = ZipUtil(zipPath)
    zipObj.get_all_xml_files()
    xmlObj = XmlUtil(zipObj.file_list)
    xmlObj.parse_xml_file()
    excelObj = ExcelUtil(
        xmlObj.fileList, xmlObj.allWbtsAndWcel, xmlObj.allTypeAndCounters
    )
    excelObj.convert_to_data_frames()
    excelObj.generate_excel(outPutPath)
    print("################### Excel File Generated : {} ###################".format(
        outPutPath))


if __name__ == "__main__":
    main()
