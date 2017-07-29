# CardiB_api
an api to get a random BAR from cardi b's already impressive catalogue of quotables
Unfortunately azlyrics.com has some webcrawling blockers, so right now theres just a couple measly text files sitting on a server somewhere. But hopefully there are enough bars to get this off the ground.

Recently Added:

james baldwin
jay-z
nas
tupac
kanye west
lauryn hill
inspirational quotes for programming


# To Do
- Or specify a genre
- Add deeper catalogue for each artist
- see issues

# Live at http://cardibbars.pythonanywhere.com/api/v1

If you send a `GET` request api will return a quote from any of those categories/people

If you send a `POST` include a JSON body with the following format:

```
{
    method:"getQuote",
    category: ['jay_z','inspirational_code']
}
```

The format shown above will choose a random quote from either jay-z or the inspiring coding quotes catalogue.

The total list of options are as follows:

```
'james_baldwin'
'cardi_b'
'jay_z'
'nas'
'inspirational_code'
'kanye_west'
'lauryn_hill'
'tupac'
```


