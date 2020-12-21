# Misctools-DataScience
## Part 1: NYC-dashboard
Mostly playing around with Bokeh, the task was to develop a dashboard allowing city leaders to explore the discrepancy in service across zipcodes, 
using a derivate of this dataset:
[https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9). So this is code for a Bokeh Dasboard that has two dropdown selectors that allow you to pick two separate zipcodes. 
#### My very clunky Bash commands for cleaning:
`cut -d, -f1-3,9 < nyc_311_limit.csv >clean.csv`  
`awk -F, '$2~/.*2020/' clean.csv > d.csv    `
`cat d.csv | sed -e '/,,/d' > e.csv `
 `awk -F, '$4~/[0-9]{5}/' e.csv > f.csv `     
`vim header.csv  `
`cat header.csv f.csv > final.csv`

