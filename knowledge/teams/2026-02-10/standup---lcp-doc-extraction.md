# Teams Chat — Standup - LCP Doc Extraction

## 10:29 - Katyayani Lal
> Also when the documents are attached, the count is not displayed
> 
> <img src="https://graph.microsoft.com/v1.0/chats/19:meeting_NjA0MDcyYmYtNzI5YS00ZmIwLTlkZDYtYzZkY2U0NTQ4YmE0@thread.v2/messages/1770719389484/hostedContents/aWQ9eF8wLXd1ay1kNC1jYjBmYTYzNDk1ZjZhODJhMWQxMjc2MTY2OTI5YTlmNCx0eXBlPTEsdXJsPWh0dHBzOi8vdWstYXBpLmFzbS5za3lwZS5jb20vdjEvb2JqZWN0cy8wLXd1ay1kNC1jYjBmYTYzNDk1ZjZhODJhMWQxMjc2MTY2OTI5YTlmNC92aWV3cy9pbWdv/$value" width="1233.0801104972375" height="250" alt="image" itemid="0-wuk-d4-cb0fa63495f6a82a1d1276166929a9f4">
> 
> <attachment id="1770718577362"></attachment>

## 10:17 - Ajay Gannamaneni
> <attachment id="1770718577362"></attachment>
> Will look into it 
> I remember fixing it but will let you know in 10mins

## 10:16 - Katyayani Lal
> @Ajay, While testing, when **only the email body** is provided (no PDF), the extraction takes a very long time, it's been ~30 minutes and is still not completed.
> 
> <img src="https://graph.microsoft.com/v1.0/chats/19:meeting_NjA0MDcyYmYtNzI5YS00ZmIwLTlkZDYtYzZkY2U0NTQ4YmE0@thread.v2/messages/1770718577362/hostedContents/aWQ9eF8wLXN1ay1kNC1jMjRhZjRiNzc2MzNiNjVkNWYyZWMwMDkzNzI2NTY4Nyx0eXBlPTEsdXJsPWh0dHBzOi8vdWstYXBpLmFzbS5za3lwZS5jb20vdjEvb2JqZWN0cy8wLXN1ay1kNC1jMjRhZjRiNzc2MzNiNjVkNWYyZWMwMDkzNzI2NTY4Ny92aWV3cy9pbWdv/$value" width="1233.0801104972375" height="250" alt="image" itemid="0-suk-d4-c24af4b77633b65d5f2ec00937265687">
> 
> However, when the email **body + PDF** are provided together, extraction completes, but the values are picked only from the **PDF**, not from the email body.
> 
> <img src="https://graph.microsoft.com/v1.0/chats/19:meeting_NjA0MDcyYmYtNzI5YS00ZmIwLTlkZDYtYzZkY2U0NTQ4YmE0@thread.v2/messages/1770718577362/hostedContents/aWQ9eF8wLXd1ay1kNC01NjY5YzEwZDRhMzI1M2RkYmM5M2M0MGY4MTI0NTg5NSx0eXBlPTEsdXJsPWh0dHBzOi8vdWstYXBpLmFzbS5za3lwZS5jb20vdjEvb2JqZWN0cy8wLXd1ay1kNC01NjY5YzEwZDRhMzI1M2RkYmM5M2M0MGY4MTI0NTg5NS92aWV3cy9pbWdv/$value" width="1264.236111111111" height="250" alt="image" itemid="0-wuk-d4-5669c10d4a3253ddbc93c40f81245895">




## 12:30 - Timon Wan
> <attachment id="1770726507104"></attachment>
> 
> Values may look like so in the email:
> 
> SCHEDULED REDEMPTION DATE: July [•], 2029 (or if such day is not a Business Day, on the next succeeding Business Day)

## 12:29 - Ajay Gannamaneni
> we can use agents in AIfoundry

## 12:29 - Ajay Gannamaneni
> but if it makes more sense to configure it as string it as string when it comes to normalisation i can always call an agent to normalise it and get the value as expected

## 12:28 - Ajay Gannamaneni
> <attachment id="1770726371929"></attachment>
> 
> i have written in python to normalise whatever the value we extract from the AI we will normalise it to nearest value by fuzzy matching
> 
> for dates Analyser itself is configured as date for most

## 12:26 - Navsheen Koul
> <attachment id="1770726288267"></attachment>
> 
> multiple entries for that fields should be accepted and if thats not possible for now then atleast it should show up in the hamburger icon otherwise it can be classified as wrong input or AI not extracting the data properly

## 12:26 - Timon Wan
> @Ajay Gannamaneni how set is the datamodel in SQL atm?
> 
> i.e. some dates that come in would not necessarily be fixed dates.

## 12:24 - Timon Wan
> <attachment id="1770725867536"></attachment>
> 
> No idea what that means.
> 
> I'm going to focus on NEW CAT BOND email, since that has single class

## 12:17 - Navsheen Koul
> <attachment id="1770723959666"></attachment>
> 
> <img alt="image" src="https://graph.microsoft.com/v1.0/chats/19:meeting_NjA0MDcyYmYtNzI5YS00ZmIwLTlkZDYtYzZkY2U0NTQ4YmE0@thread.v2/messages/1770725867536/hostedContents/aWQ9eF8wLXd1ay1kMS1iOTQwODg4NDAxZjM2OTBlY2U1N2ExYWZhYTk4YTA5Mix0eXBlPTEsdXJsPWh0dHBzOi8vdWstYXBpLmFzbS5za3lwZS5jb20vdjEvb2JqZWN0cy8wLXd1ay1kMS1iOTQwODg4NDAxZjM2OTBlY2U1N2ExYWZhYTk4YTA5Mi92aWV3cy9pbWdv/$value" width="1213.022508038585" height="250" itemid="0-wuk-d1-b940888401f3690ece57a1afaa98a092" />

## 12:14 - Navsheen Koul
> <attachment id="1770725315709"></attachment>
> 
> yes, @Jake can add you

## 12:08 - Timon Wan
> @Navsheen Koul Do we have a LCP Teams?
> 
> Would be nice to have all the test documents and such in a folder somewhere
