# Teams Chat — Standup - LCP Doc Extraction

## 05:19 - Navsheen Koul
> <p>Morning <at id="0">Ajay</at>, <at id="1">Katyayani</at>&nbsp;how are we looking?</p>


## 05:34 - Navsheen Koul
> <p>do you think its had a positive impact on AI extraction?</p>

## 05:31 - Ajay Gannamaneni
> <div>
> <attachment id="1770700765294"></attachment>
> I updated to another version of analyser <br>
> I will do a unit test and inform katyayini for testing</div>


# Teams Chat — Standup - LCP Doc Extraction

## 06:24 - Navsheen Koul
> <p><at id="0">Ajay</at>&nbsp;I want to update LCP ADO with the tickets retrospectively but my password had expired so i created a new one. However its now saying that sign in failed due to change in email or password. Tarun has suggested that the lanware IT team needs to manually allow me to sign in again. Is that what it is?</p>

## 06:41 - Ajay Gannamaneni
> <attachment id="1770701650129"></attachment>
> <p>testing it i will let you know</p>

## 06:40 - Ajay Gannamaneni
> <p>No idea</p>


# Teams Chat — Standup - LCP Doc Extraction

## 10:17 - Ajay Gannamaneni
> [Attachment: 1770718577362]
> Will look into it
> I remember fixing it but will let you know in 10mins

## 10:16 - Katyayani Lal
> @Ajay, While testing, when only the email body is provided (no PDF), the extraction takes a very long time, it's been ~30 minutes and is still not completed.
> [Image]
> 
> However, when the email body + PDF are provided together, extraction completes, but the values are picked only from the PDF, not from the email body.
> [Image]


# Teams Chat — Standup - LCP Doc Extraction

## 11:13 - Timon Wan
> <p><at id="0">Navsheen</at>&nbsp;<at id="1">Koul</at>&nbsp;do we expect all mandatory fields to also be present in Email?</p>

# Teams Chat — Standup - LCP Doc Extraction

## 11:34 - Timon Wan
> <p><at id="0">Ajay</at>&nbsp;<at id="1">Gannamaneni</at>&nbsp;<at id="2">Navsheen</at>&nbsp;<at id="3">Koul</at>&nbsp;In the Lion Re DAC email, I see that the email contains two classes. Class A and Class B, what should be happen in such scenarios?</p>


# Teams Chat — Standup - LCP Doc Extraction

## 11:45 - Timon Wan
> It's more than the email contains both Class A Notes and Class B Notes.
>
> Atm the analyzer seems to only expect one unless I'm mistaken

## 11:44 - Navsheen Koul
> [attachment: 1770723269588]
> whatever is in the email body should be populated first and the hamburger icon should show other values for the same field found in other locations with a precision score

## 11:43 - Navsheen Koul
> [attachment: 1770721989883]
> this question has not come up explicitly so unsure

## 11:34 - Timon Wan
> @Ajay @Gannamaneni @Navsheen @Koul In the Lion Re DAC email, I see that the email contains two classes. Class A and Class B, what should be happen in such scenarios?

## 11:13 - Timon Wan
> @Navsheen @Koul do we expect all mandatory fields to also be present in Email?

## 11:03 - Ajay Gannamaneni
> [attachment: 1770719389484]
> track this will fix it later i noticed too its not working as expected

## 11:02 - Ajay Gannamaneni
> [attachment: 1770718628307]
> this is deployed

## 10:29 - Katyayani Lal
> Also when the documents are attached, the count is not displayed
> [image]
> [attachment: 1770718577362]

## 10:17 - Ajay Gannamaneni
> [attachment: 1770718577362]
> Will look into it
> I remember fixing it but will let you know in 10mins

## 10:16 - Katyayani Lal
> @Ajay, While testing, when only the email body is provided (no PDF), the extraction takes a very long time, it's been ~30 minutes and is still not completed.
> [image]
>
> However, when the email body + PDF are provided together, extraction completes, but the values are picked only from the PDF, not from the email body.
> [image]

# Teams Chat — Standup - LCP Doc Extraction

## 12:14 - Navsheen Koul
> yes, Jake can add you

## 12:08 - Timon Wan
> Navsheen Koul Do we have a LCP Teams?
> 
> Would be nice to have all the test documents and such in a folder somewhere

## 12:03 - Navsheen Koul
> Ajay, Timon if you have questions for tayo please lmk

## 12:01 - Navsheen Koul
> Issuance Date - is it 'subject to completion'? page 2
> 
> Maturity Date - should be pulling 'redemption date' but not working. page 27.
> 
> Scheduled Maturity Date - should be 'scheduled redemption date' or 'final extended redemption date'. page 27
> 
> On Risk Date - cant find in pdf
> 
> Off Risk Date - cant find in pdf
> 
> Total Issue Size - laptop is slow, cant find
> 
> Amount Outstanding - cant find; but can find the term original principal amount
> 
> Per Occurrence Limit - retrieves 'initial exhaustion point'; confirm whether this is right ; page 48
> 
> Per Occurrence Attachment - tested and worked fine
> 
> the above is what i found when testing on 1886 pdf

## 11:59 - Katyayani Lal
> It Took a little longer, however now its extracted. Count is less than 18.

## 11:57 - Timon Wan
> Thanks

## 11:57 - Katyayani Lal
> Above fields are missing

## 11:56 - Navsheen Koul
> waiting for his response

## 11:53 - Timon Wan
> Which fields are still missing please

## 11:53 - Katyayani Lal
> Meanwhile, Ajay same issue when used NEW 144A email body with pdf


# Teams Chat — Standup - LCP Doc Extraction

## 12:42 - Ajay Gannamaneni
> <p>App side is dynamic</p>

## 12:41 - Ajay Gannamaneni
> <p>10-15mins to insert data</p>

## 12:41 - Ajay Gannamaneni
> <p>not a big change</p>

## 12:41 - Timon Wan
> <p>Thanks.</p>
> <p>Regarding the App, how hard is it to add another option to select Analyzer? Quick change?</p>

## 12:40 - Ajay Gannamaneni
> <p>for now i will change all fields to string</p>


# Teams Chat — Standup - LCP Doc Extraction

## 13:14 - Timon Wan
> Ajay Gannamaneni can you make a new dropdown option in the App for which Analyzer to use?
>
> I'm going to deploy a new version called 'catBondDocumentAnalyzerLatest'.
>
> This one will be constantly updated version

## 12:42 - Ajay Gannamaneni
> App side is dynamic

## 12:41 - Ajay Gannamaneni
> 10-15mins to insert data

## 12:41 - Ajay Gannamaneni
> not a big change

## 12:41 - Timon Wan
> Thanks.
>
> Regarding the App, how hard is it to add another option to select Analyzer? Quick change?

## 12:40 - Ajay Gannamaneni
> for now i will change all fields to string

## 12:40 - Ajay Gannamaneni
> [Attachment: 1770726776210]
>
> it stores as string

## 12:32 - Timon Wan
> Think it's a wider convo of how we go about it, but for time being, if the model returns back "July [•], 2029 (or if such day is not a Business Day, on the next succeeding Business Day)", does that get stored in the DB or breaks things since it was expected Date type but now is a String type

## 12:31 - Ajay Gannamaneni
> [Attachment: 1770726600438]
>
> i can use AI agent but result may not be accurate in this case since no date mentioned we can store it as first day of month

## 12:30 - Timon Wan
> [Attachment: 1770726507104]
>
> Values may look like so in the email:
>
> SCHEDULED REDEMPTION DATE: July [•], 2029 (or if such day is not a Business Day, on the next succeeding Business Day)

# Teams Chat — Standup - LCP Doc Extraction

## 13:23 - Timon Wan
> @Navsheen @Koul are the PDFs redacted in anyways?
>
> $[●] Series 2025-1 Class A Principal At-Risk Variable Rate Notes due July [6], 2029
>
> $[●]  <--- Is this a redaction?

## 13:20 - Timon Wan
> catBondDocumentAnalyzerLatest

## 13:20 - Timon Wan
> Yes

## 13:20 - Ajay Gannamaneni
> is this exact name?

## 13:20 - Ajay Gannamaneni
> catBondDocumentAnalyzerLatest

## 13:20 - Ajay Gannamaneni
> give me analyserId

## 13:14 - Timon Wan
> @Ajay @Gannamaneni can you make a new dropdown option in the App for which Analyzer to use?
>
> I'm going to deploy a new version called 'catBondDocumentAnalyzerLatest'.
>
> This one will be constantly updated version

# Teams Chat — Standup - LCP Doc Extraction

## 13:44 - Timon Wan
> Thanks, looks like it to me, but just wanted to make sure

## 13:44 - Navsheen Koul
> <attachment id="1770729807981"></attachment>
> have asked

## 13:23 - Timon Wan
> <at id="0">Navsheen</at> <at id="1">Koul</at> are the PDFs redacted in anyways?
> 
> **$[●] Series 2025-1 Class A Principal At-Risk Variable Rate Notes due July [6], 2029**
> 
>  
> **$[●]  **<--- Is this a redaction?

## 13:20 - Timon Wan
> catBondDocumentAnalyzerLatest

## 13:20 - Timon Wan
> Yes

## 13:20 - Ajay Gannamaneni
> is this exact name?

## 13:20 - Ajay Gannamaneni
> catBondDocumentAnalyzerLatest

## 13:20 - Ajay Gannamaneni
> give me analyserId

## 13:14 - Timon Wan
> <at id="0">Ajay</at> <at id="1">Gannamaneni</at> can you make a new dropdown option in the App for which Analyzer to use?
> I'm going to deploy a new version called 'catBondDocumentAnalyzerLatest'.
> This one will be constantly updated version

## 12:42 - Ajay Gannamaneni
> App side is dynamic



## 14:31 - Navsheen Koul
> <p>how many of these are mandatory fields?</p>

## 14:30 - Katyayani Lal
> <p>I have tested the combination of Email and docs for extraction,</p>
> <p>&nbsp;the highest count we have got so far is for the <strong>NEW CAT BOND email body + Preliminary pdf </strong>which is 18 fields. Other than that I have updated the sheet regarding the UI issues that were found while testing.</p>

## 14:26 - Navsheen Koul
> <p>sorry should have mentioned before, could you give me more outcome based updates i.e. what is better and works now for the demo on thursday</p>

## 14:25 - Ajay Gannamaneni
> <attachment id="1770733073767"></attachment>
> <p>initial i was working to create finalV2 version analyser.</p>
> <p>issue reported by Katyayani no attachment one</p>
> <p>created V3 version in backend</p>
> <p>now i am working on breaking the pdf into chunks</p>

## 14:17 - Navsheen Koul
> <p><at id="0">Ajay</at>, <at id="1">Katyayani</at>&nbsp;before you log off for the day could you add an update here please.</p>

## 14:12 - Katyayani Lal
> <p>I can see data only from one page of the PDF, so it looks like the extraction happened from just a single page.</p>
> <p><img alt="image" src="https://graph.microsoft.com/v1.0/chats/19:meeting_NjA0MDcyYmYtNzI5YS00ZmIwLTlkZDYtYzZkY2U0NTQ4YmE0@thread.v2/messages/1770732726686/hostedContents/aWQ9eF8wLXN1ay1kNC00NDM2NDg5ODU1YmM1MmYyMWM2OWI4NjEyMWZiNmRlMyx0eXBlPTEsdXJsPWh0dHBzOi8vdWstYXBpLmFzbS5za3lwZS5jb20vdjEvb2JqZWN0cy8wLXN1ay1kNC00NDM2NDg5ODU1YmM1MmYyMWM2OWI4NjEyMWZiNmRlMy92aWV3cy9pbWdv/$value" itemid="0-suk-d4-4436489855bc52f21c69b86121fb6de3" width="800" height="238"></p>

## 14:10 - Katyayani Lal
> <attachment id="1770724315144"></attachment>
> <p>Used the same combination to test with V3. 8 fields listed below are extracted:</p>
> <ul>
> <li>Issuance Date</li><li>Maturity Date</li><li>SPV</li><li>Bond Series</li><li>Trigger Type</li><li>Sponsors</li><li>Lead Managers</li><li>Structures</li></ul>

## 14:02 - Timon Wan
> <p><at id="0">Katyayani</at>&nbsp;<at id="1">Lal</at>&nbsp;can you test using this V3&nbsp;</p>
> <p>The NEW CAT BOND please</p>

## 13:59 - Timon Wan
> <p>Yup, can see</p>

## 13:58 - Ajay Gannamaneni
> <p>in APP in dropdown we will see it as V3</p>
