# API Endpoint document

## /api/users/
* GET:list all users (only admin can get all users ,other just can get himself)
* POST:Registration , and get JWT Token to login.
    * username
    * email
    * password
    * first_name
    * last_name
    * student_id
    * address
    * birthday
    * phone_number
    * is_staff(admin only)
    * unban_date(admin only)
    

## /api/users/{username}
* GET: get user's profile
* PUT: update user's profile
* DELETE : delete user , only admin can do

## /api/users/login
* POST:using username and password to exchange JWT Token
    * username
    * password

## /api/api-token-refresh
* POST : using existing token which hasn't expired to
exchange a new token.
    * token

## /api/api-token-verify
* POST : check token validity
    * token

## /api/books/
* GET : List All Books
    * /api/books/?ISBN={ISBN} get book using ISBN
* POST : Add a book (admin only)

## /api/books/{id}
* GET : Retrieve Book by id
* PUT: Update Book(admin only)
* DELETE : remove book (admin only)

## /api/barcodes/
* GET : List all barcodes
* POST : Create a barcode(admin only)


## /api/barcodes/{barcode}
* GET : Retrieve barcode
* PUT : Update (admin only)
* DELETE: Remove (admin only)


## /api/borrowinfos/
* GET : List All Borrow Information
    * /api/borrowinfos?username={username}  
        filter the user's borrow informations
* POST : Create

## /api/borrowinfos/{id}/
* GET : Retrieve Borrow Information
* PUT : Update (admin only)
* DELETE : Remove (admin only)

