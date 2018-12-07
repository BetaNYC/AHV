# AHV Dashboard
The [After Hours Variance (AHV) Dashboard](https://beta.nyc/products/ahv-dashboard/) is a tool to track the location and saturation of after-hours variance permits issued in New York City community districts. The tool empowers community boards and district offices to advocate for better quality of life conditions in their districts.

Currently, data about the number and location of after-hours variances issued by the Department of Buildings is difficult to access. Someone can query the Department of Buildings website for the after-hours variances issued to a specific address, but to create a map that shows the saturation of permits awarded in a community district, that individual would need to query the website for every address in that district. 

We’ve created a [script](https://github.com/BetaNYC/AHV/blob/master/AHVScraper.py) that scrapes the Department of Buildings website to collect data about after-hours variances awarded to each building in a community district. We’ve also created a dashboard to visualize this data. The dashboard compares the number of after-hours variances awarded to each address to the 311 noise complaints about after-hours construction made at the same locations. It also visualizes how businesses applying for a permit responded to the question “Is this site within 200 ft. of a residence,” enabling boards to audit how applicants are responding to the question.

We’ve scraped the data for Manhattan Community District 1 (June 28, 2018) and 2 (June 19, 2018) and are working to scrape the data for Manhattan Community District 7 (August 13, 2018). The Manhattan Borough President has also sent a letter to the Department of Buildings requesting that this data be made publicly available in an accessible format, so that we may build the dashboard for all districts in NYC.

## How to Access the Tool

AHV Dashboard can be accessed at: [https://betanyc.github.io/AHV/](https://betanyc.github.io/AHV/).

## How to Contribute 
* File an issue via this [repo's issue cue](https://github.com/BetaNYC/AHV/issues).
* Request a feature via this [repo's issue cue](https://github.com/BetaNYC/AHV/issues).
* Comment on issues. 
* Write code to fix issues or to create new features. When contributing code, please be sure to: 
  * Fork this repository, modify the code (changing only one thing at a time), and then issue a pull request for each change.
  * Test your code locally before issuing a pull request. 
  * Clearly state the purpose of your change in the description field for each commit.

## Scraping AHV Data

### Requirements:
* Python 2.7
* Selenium
* Requests
* Beautiful Soup 4
* lxml
* Be to download and unzip geckodriver at [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases) and copy it into your bin folder.

The python script in this repository is designed to import a CSV file of DOB Building Identification Numbers (BINs) and, for each BIN, concatenate the BIN to a BISWeb URL that lists links to each BIN's public AHV permit files. (Format: http://a810-bisweb.nyc.gov/bisweb/AHVPermitsQueryByNumberServlet?requestid=1&allkey=' + BIN + '&fillerdata=A') From the page listing links to AHV permit files, it then navigates to the link for each AHV permit file and scrapes the data about the AHV permit. From the page listing links to AHV permit files, it checks if there are multiple pages of AHV links listed and, if so, clicks to follow to the next page until there are no more 'next pages'. The data scraped about each permit is stored as a row in a new file. 

The list of BINs can be collected from the [DOB's Building Footprints Shapefile](https://data.cityofnewyork.us/Housing-Development/Building-Footprints/nqwf-w8eh). A column list of BINs should be saved in a separate .csv, and the name of this file should be filled into (line 27) (with open('FILL') as csvfile:). I filtered to the BINs in a single community district by importing both the Building Footprints shapefile and the [Community District](https://data.cityofnewyork.us/City-Government/Community-Districts/yfnk-k7r4) shapefile into QGIS and then selecting all building polygons that overlapped with a community district by drawing a polygon select by hand. Even when filtering to one community board, the script takes at least 6 hours to run. 

Note that the DOB's site is very slow and eventually the script times out. However, by the time of the timeout, the already scraped data is already written to "After_Hours_Variances.csv". When a timeout would occur, I would copy all of the already scraped data into a new file. Then I would check the last BIN scraped by copying the URL (output to my console) into BISWeb and checking the listed BIN at this URL. Next I would locate that BIN in my input CSV file, remove all of the BINs listed prior to it, and re-run the script. I would continue doing this until reaching the final BIN and then merge the data in all of the output files (copied after the timeout) together. Since there may be several rows for one BIN, it is likely that there will be some repeated rows for the last BIN scraped before each timeout and the first BIN scraped after each timeout when you merge these files together. Be sure to remove the duplicates at the end. 

## Visualizing the Data in Tableau

The tableau worksheets in this repository can be updated with freshly scraped AHV data. First, download a worksheet in this repository and open it in Tableau Public. Import "After-Hours-Variances.csv" as a text file. Also, import the DOB's Building Footprints shapefile filtered to the BINs represented in "After_Hours_Variances.csv". Join these two files by the BIN in Tableau Public (you may need to change the data type of on of the BIN columns to match the other BIN column) Then navigate to the tab 'AHV Map'. In the main navigation, click Data>>Replace Data Source. Replace the data with your newly joined file. To update the Noise Map, navigate to the [311 Service Requests from 2010 to Present dataset](https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9), and using Socrata, filter the data to Descriptor (Noise: Construction Before/After Hours (NM1)) and the Created Date (before the day you scraped the data). Download the filtered dataset as a CSV and import it as a text file into Tableau Public. Then navigate to the tab 'Noise'. In the main navigation, click Data>>Replace Data Source. Replace the data with your new 311 file. 

Navigate to the tab 'Story 1' and change the title to reflect the geography represented and then save the workbook to Tableau Public.

## Adding the Visualization to the index.html
Once the visualization is saved to Tableau Public, you can click the share button below the visualization and copy and paste the embed code into index.html. 


### Initial Commit v0.5

* On page 1, users can view a map of the saturation of noise complaints made to 311 about before/after-hours construction, next to a map of the buildings that have been issued AHVs (colored according to the number they've been awarded.
* On page 2, users can click on a building to view a bar chart showing, by month, how many applicants responded yes to the question "Is this site within 200 ft. of a residence" for the building vs. how many responded no. Users can also view a tree map of which businesses have been awarded AHVs for the building. Clicking on a bar in the bar chart will filter the business tree map to those businesses that responded yes/no during that month. Clicking on a business in the tree map will filter the bar chart to display only the way the selected business responded to the question over a series of months. 
* On page 3, users can click on a building to view a tree map of which businesses have been awarded AHVs for the building. Users can also click on a business in the tree map to view for which buildings the business has been awarded AHVs.
* On page 4, users can click on a building to view a list of statuses for AHV applications for that building (including whether the AHVs were issued, denied, revoked, withdrawn, or in process). Users can also click on a AHV application status to learn which buildings have AHVs at that status. This allows users to check where AHVs have been revoked or denied.
* On page 5, users can click on a building to view a list of reasons for AHVs were awarded for that building. Users can also click on a reason in the list to view which buildings AHVs were awarded for that reason.
* On each page, users can filter all maps and graphs to a particular date range between 2011 and the date the data was scraped.
* On each page, users can hover over a building to view its BIN, the number of AHVs it has been awarded, the number of days it has been permitted to conduct after-hours construction, and the addresses on file for the building.  

## Copyrights 

Please see [license] file for details.
 * Non-code, Creative Commons Attribution 4.0
 * Code, GNU General Public License
