# JOBPORTAL

## Project description:
[jobportal] is a web app developed for job searching and recruitment within the gastronomy sector in the Czech Republic. It allows users to browse and apply for job opportunities in their selected regions. Registered users  can post job listings for potential candidates.

This project was created as part of the final examination for the "Python from Scratch" programming course provided by Software Development Academy.

Authors: Juraj Miškolczi, Livia Nowak Abdul, Nicole Taudy


## Project outline: 

- [x] client registration
- [x] client login
- [ ] ads handling by client
    - [x] create
    - [ ] view
    - [ ] edit
    - [ ] delete
- [ ] ads view on homepage
- [x] ads detail on click
- [ ] ads search and filter by location and position
- [x] inquiry - form submit (plus attachment)
- [ ] PayPal - mock in user account
- [x] ad post
- [x] price list view
- [ ] notification - confirmation of purchase

## Lower priority:
- [ ] job portal info
- [ ] applicants replies in client's account
- [ ] localization
- [ ] ads posting without registration
- [ ] ads highlight on front page on request (paid)

## Databases:

- [x] Client
   - [x] business type
   - [x] address
   - [x] city
   - [x] district
   - [x] business name
   - [x] VAT number 
   - [x] logo
   - [x] contact
       - [x] email
       - [x] phone number
   

- [x] Business type
   - [x] name


- [x] Advertisement
   - [x] position
   - [x] title
   - [x] text content
   - [x] salary
   - [x] client id 
   - [x] created
 
  
- [x] Position
    - [x] name


- [x] Region
    - [x] name


- [x] District
    - [x] name
    - [x] region id


![jobportal_ERD.png](jobportal_ERD.png)