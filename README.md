# Meade Maintenance App

## Contents

1. [Project Overview](#project-overview)
2. [Project Inception](#project-inception)
3. [UX](#ux)
4. [Features](#features)
5. [Technologies](#technologies)
6. [Testing](#testing)
7. [Running Locally](#running-locally)
8. [Deployment](#deployment)
9. [Project Outcome](#project-outcome)
10. [Credits](#credits)

## Project Overview

The Meade Maintenance App is a bespoke web based application, designed for Meade Farm Group, that allows the maintenance team and their managers to record and maintain stock records and job records. The project uses *Django*, *PostgresQL*, *Heroku* and *AWS S3*. The project was requested by the maintenance team who required an easy to use, mobile, responsive application for recording and maintaining stock and job records.

Meade Farm Group is a fresh goods processor based in the Republic of Ireland, servicing the retail food sector, supplying fresh goods to the likes of Lidl and Aldi, amongst others. The maintenance/engineering teams at the company are involved in the general maintenance of all the machines in the factory, utilities in the offices and developing new areas and projects. Due to this wide range of responsibilities and the often *ad-hoc* nature of their work an app was required that allowed the team to record and maintain records of their work quickly and easily while on the job as well as being intuitive, giving users notifications of outstanding jobs to be done.

Recording and maintaining stock records and job records and analayzing the trends and resources being used by different departments was key to management too to be able to make informed decisions.

## UX

### Project Goals

The goal of this project is to create an application that allows maintenance/engineering users to record and maintain job records as well as stock records. The interface should be quick and easy to use, bearing in mind that the users often will need to record information on the application while on the job. The stock system should allow stock to be received in, transferred to a user, and assigned to a job. It should also allow. All jobs and stock movements should be assigned to a department/product line so that reports can be build to analyze the resources being spent used by the different departments/product lines. The UI should be simple, easy to use and navigate, and feature unique functionalities depending on the user that is logged in *(Admin, Manager, General Operative, etc.)* The app should also communicate effectively with the users, informing them when they've been assigned a job/have outstanding tasks via notifications when on mobile.

### User Goals

* Record time against jobs
* Stock management
* Allocate resources to jobs
* View outstanding jobs
* View reports about resources being consumed
* Easy to use UI when working
* Notifications system that informs users of new jobs that have been assigned

### User Stories

* As a maintenance engineer, I need to be able to easily view my outstanding jobs while on the production floor. I also need to be able to quickly create and record time against jobs. I also need to be able to create unscheduled *ad hoc* jobs. I also want to be notified of any new jobs that are assigned to me.
* As a maintenance manager, I need to be able to create jobs and assign them to users. I also need jobs to be automatically generated for different assets at specified time intervals. I also need to be able to view reports detailing resources used by different departments/product lines. I also need to be able to see pending requests and approve them. I also want to be able to assign priorities to jobs.
* As a stock controller, I need to be able to accurately maintain stock records. I need to be able to receive stock in and then assign it to users who can then assign it to jobs. I'd also like to be notified when stock quantities fall below a certain threshold. I'd also like to be able to assign items barcodes and be able to scan those barcodes when assigning stock.
* As a production supervisor, I need to be able to request jobs by maintenance. I should be able to specify the area where the problem is, details of the problem and I should be notified whether the request has been accepted or not.
* As a commercial buyer, I need to be able to see reports detailing how much resources/time is being consumed by my product lines so that I can make informed decisions about the viability of the products.

