# AHV Dashboard
The After Hours Variance (AHV) Dashboard is a tool to track the location and saturation of after-hours variance permits issued in New York City community districts. The tool empowers community boards and district offices to advocate for better quality of life conditions in their districts.

Currently, data about the number and location of after-hours variances issued by the Department of Buildings is difficult to access. Someone can query the Department of Buildings website for the after-hours variances issued to a specific address, but to create a map that shows the saturation of permits awarded in a community district, that individual would need to query the website for every address in that district. 

We’ve created a [script](https://github.com/BetaNYC/AHV/blob/master/AHVScraper.py) that scrapes the Department of Buildings website to collect data about after-hours variances awarded to each building in a community district. We’ve also created a dashboard to visualize this data. The dashboard compares the number of after-hours variances awarded to each address to the 311 noise complaints about after-hours construction made at the same locations. It also visualizes how businesses applying for a permit responded to the question “Is this site within 200 ft. of a residence,” enabling boards to audit how applicants are responding to the question.

We’ve scraped the data for Manhattan Community District 1 (June 28, 2018) and 2 (June 19, 2018) and are working to scrape the data for Manhattan Community District 7 (August 13, 2018). The Manhattan Borough President has also sent a letter to the Department of Buildings requesting that this data be made publicly available in an accessible format, so that we may build the dashboard for all districts in NYC.

## File an Issue 
We're tracking all issues via this [repo's issue cue](https://github.com/BetaNYC/AHV/issues).

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
