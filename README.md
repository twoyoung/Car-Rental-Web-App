# car-rental-webapp

## Log in methods:
http://2young.pythonanywhere.com/
* as admin:
  * username: admin
  * password: admin
* as staff:
  * username: staff1
  * password: staff1
* as customer:
  * username: customer1
  * password: customer1

## This is a web app for a car rental company with the following functions:
* client-side real-time form validation:
  * Immediate validation feedback: As the user types in the form field, the input is validated in real time, which means that the user could immediately see any errors in their input, rather than having to wait until they submit the form to find out that they have made a mistake.
  * Disabled submit button: The submit button is disabled until all inputs are valid and all required fields are filled, which will prevent the user from submitting the form with invalid data.
* role-based access control: admin, staff and customer are granted different levels of permissions based on their role. If a user attempts to access a page that they are not authorized to view, they will be redirected to an unauthorized page.
* customer register new account
* login/logout system
* users edit own profile/ change password
* role-based dashboards and functions design
* user/car management:
  * admin: list/check/add/edit/delete customer/staff/cars
  * staff: list/check/add/edit/delete cars, check customer profile
  * customer: list/check available cars
* responstive web design
  

## Current bug that hasn't been fixed:
* Some functions and buttons such as the filter on customer dashboard and list icon on the header hasn't been achieved yet due to the limit of time.
