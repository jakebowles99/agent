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
