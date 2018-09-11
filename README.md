# CardiB_api
An api to get a random BAR from an variety of different artists. They are listed below.
The name of the service came because Cardi B inspired this project about a year ago because literally everyone of her songs had hella quotables in it. Fortunately the service has expanded to include a number of other artists as well some quotes from other notable writers and thought leaders such as James Baldwin.


# To Do
- Or specify a genre
- Add deeper catalogue for each artist
- see [issues](https://github.com/weallwegot/CardiB_api/issues)

# Live at http://cardibbars.pythonanywhere.com/api/v1

If you send a `GET` request api will return a quote from any of those categories/people

If you send a `POST` include a JSON body with the following format:

```
{
    method:"getQuote",
    category: ['jay_z','earlsweatshirt','inspirational_code']
}
```

The format shown above will choose a random quote from either jay-z or the inspiring coding quotes catalogue.

The total list of options are as follows:

```
'james_baldwin'
'cardi_b'
'jay_z'
'jayz'
'2pac'
'nas'
'inspirational_code'
'kanye_west'
'lauryn_hill'
'tupac','2pac'
'kehlani'
'kendricklamar'
'absoul'
'asaprocky'
'lilboosie'
'bigpun'
'liluzivert'
'bigsean'
'lilwayne'
'camron'
'lilyachty'
'cardi'
'logic'
'ludacris'
'chancetherapper'
'lupefiasco'
'common'
'macmiller'
'domkennedy'
'meekmill,
'drake'
'nas'
'earlsweatshirt'
'fatjoe'
'nickiminaj'
'future'
'notorious'
'game'
'outkast'
'goldlink'
'pushat'
'guccimane'
'rickross'
'schoolboyq'
'isaiahrashad'
'ti'
'jadakiss',     
'tylerthecreator'
'vicmensa'
'jayz'
'vincestaples'
'jcole'
'wale'
'jid'
'west'
'joeybada'
'yg'
'kanye'
'youngjeezy'
```


## Contributing

Its still pretty early but if you have suggestions, thoughts, feedback, criticism, etc feel free to open a PR or submit an Issue. 

Thanks in advance :blush:

--------------------------------------------------------------------------

#### Donating

If ya feeling generous, hollr @ the kid :heart:

https://www.paypal.me/hijodelsol

**BTC: 3EbMygEoo8gqgPHxmqa631ZVSwgWaoCj3m**

**ETH: 0x2F2604AA943dB4E7257636793F38dD3B1808A9e7**

**LTC: MQVgzNDgw43YzyUg3XmH3jQ7L8ndVswmN3**