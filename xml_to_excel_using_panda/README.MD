#Script to read certian values from xml and output to an excel file with multiple sheet using python panda.


The objectives of this test are to write a piece of code in PHP or Python (select which language you prefer to use) that:

1.          Opens all xml files (attached in the compressed file) from the determined directory: c:/temp/



2. Reads the title of all the xml files transmitted one by one and load the files titles into a  "Results" csv or excel file (refer to the populated output Result file and format below)

3. Reads the date, time and measurement duration inside the file and load them in the csv or excel (see result excel file attached)




4. Reads the WBTS and the WCEL and loads them in the csv or excel

5. Reads all the types and all the counters and loads them one by one in the csv or excel

6. Reads the values of all the counters and loads them in the csv or excel

that’s it !

See below the detailed description where to find the information in the files, refer also to the excel file where you will find the information extracted,

Date, start time and duration are in the tag <PMSetup  startTime

<PMSetup  startTime="2021-04-23T14:00:00.000+00:00:00" interval="60 »> in green the information to extract

You could put the extraction in the sheet FILES

BTS and Cells are in the tag <DN

<DN><![CDATA[PLMN-PLMN/RNC-10/WBTS-4962/WCEL-49621]]></DN> in green the information to extract

You could put the extraction in the sheet  INFO1

Types, Counters and their values are in tag <PMTarget

<PMTarget  measurementType="HSDPA_WBTS"> in green the information to extract

        <M5000C0>100654</M5000C0> in green the information to extract

        <M5000C1>8334</M5000C1> in green the information to extract

        <M5000C2>2448</M5000C2> ...

        <M5000C3>752</M5000C3>

        <M5000C4>313</M5000C4>

        <M5000C5>129</M5000C5>

        <M5000C6>0</M5000C6>

        <M5000C7>97741</M5000C7>

        <M5000C8>0</M5000C8>

        <M5000C9>714</M5000C9>

        <M5000C10>840</M5000C10>

        <M5000C11>1505</M5000C11>

        <M5000C12>1819</M5000C12>

        <M5000C13>3628</M5000C13>

You could put the extraction in the sheet  INFO2,  note that you will find several measurement types,

      <PMTarget  measurementType="HSDPA_WBTS »>  in green the information to extract

      <PMTarget  measurementType="Cell_Throughput_WBTS">

      <PMTarget  measurementType="HSDPA_WBTS">

      <PMTarget  measurementType="Cell_Throughput_WBTS">

      <PMTarget  measurementType="HSDPA_WBTS">

      <PMTarget  measurementType="Cell_Throughput_WBTS">

      <PMTarget  measurementType="HSDPA_WBTS">

      <PMTarget  measurementType="Cell_Throughput_WBTS">

      <PMTarget  measurementType="HSDPA_WBTS">

      <PMTarget  measurementType="Cell_Throughput_WBTS">

      <PMTarget  measurementType="HSDPA_WBTS">

      <PMTarget  measurementType="Cell_Throughput_WBTS »>

      

Requirements
    pip 20.2.3
    Python 3.8.7

Execute script

    pip install -r requirements.txt
    python xmlData.py '<Zip File Path>' '<Output File Path>'

Example
    python xmlData.py 'Archive.zip' 'ResultFile.xlsx'

    or

    python xmlData.py 'c:/temp/Archive.zip' 'ResultFile.xlsx'