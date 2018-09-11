# CardiB_api
An api to get a random BAR from an variety of different artists. They are listed below.
The name of the service came because Cardi B inspired this project about a year ago because literally everyone of her songs had hella quotables in it. Fortunately the service has expanded to include a number of other artists as well some quotes from other notable writers and thought leaders such as James Baldwin.

In case you are using this at work there is also an option called "safe for work" that can be enabled by passing in "sfw" as an entry in the category array. Sending "sfw" alone will get you any random quotable but will make sure it doesn't include curse words. If you send "sfw" in conjunction with specific artists you will only get quotes from those artists but again without any curse words. Not specifying "sfw" means you are open to the full variety of colorful language included within the API.


# To Do
- Or specify a genre
- see [issues](https://github.com/weallwegot/CardiB_api/issues)

# Live at http://cardibbars.pythonanywhere.com/api/v1

If you send a `GET` request api will return a quote from any of those categories/people (curses words are highly probable)

If you send a `POST` include a JSON body with the following format you are indicating to the api that you wont a quote from jay-z, earl sweatshirt, or the inspirational coding quotes catalogue but you don't mind curse words:

```
{
    method:"getQuote",
    category: ['jayz','earlsweatshirt','inspirational_code']
}
```

Another `POST` request format example, in this example you only want quotes from tyler the creator but you don't want any offensive language:

```
{
    method:"getQuote",
    category: ['sfw','tylerthecreator']
}
```

And one more `POST` example for clarity; here we are indicating that we are open to quotes from any of the available sources, as long as they don't contain offensive language:

```
{
    method:"getQuote",
    category: ['sfw']
}
```


The total list of options are as follows:

```
'sfw'
'james_baldwin'
'cardi_b'
'jayz'
'2pac'
'nas'
'inspirational_code'
'kanye_west'
'lauryn_hill'
'2pac'
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
'meekmill'
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
'jadakiss'
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