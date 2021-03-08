SpeedEats: https://speed-eat-test.herokuapp.com/done_voting/1

    SpeedEats is a tool that uses the Yelp Api to help groups of people
    locate places to eat near them that all are aggreeable to.

    A special member known as the party leader will create a party object that contains
    an address as a central point around which the resturaunts will be found

    Once the party has been initailized, the server will grab a number of resturaunts near that address from the Yelp API and this will ask all the members to vote yay or nay on each resturaunt.

    Once voting is done, the website will display the winner/winners to all party members.

    You will need to get a YELP_CLIENT_ID and YELP_KEY from the Yelp developer website, then include them by those names in a file called 'secret.py' in your root directory, or set it as an environment variable if running on a remote server like heroku.