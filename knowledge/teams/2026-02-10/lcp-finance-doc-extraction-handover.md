# Teams Chat — LCP Finance Doc Extraction Handover

## 09:38 - Navsheen Koul
> <attachment id="218111a8-0c17-4056-96e7-ff5725bf9d9a"></attachment>

## 09:39 - Navsheen Koul
> Sheet to add bugs - https://synapxltd-my.sharepoint.com/:x:/g/personal/ajay_gannamaneni_synapx_com/IQDbrR2pZFK3TpNUdEWRLqqEAfqoGdWUDxWc7xSipgcaT-o?e=6oG9b7

## 09:42 - Ajay Gannamaneni
> Breakdown:
> Document 1: Email_2026-02-06.pdf
> - Time taken: 9.45 seconds
> - Total fields: 29; extracted: 7; pending: 22; confidence issue: MaturityDate
> Document 2: Lion Re DAC 2025-1 Investor Presentation.pdf
> - Time taken: 25.02 seconds
> - Total fields: 29; extracted: 7; pending: 22; confidence issue: MaturityDate
> Document 3: Lion Re DAC - Series 2025-1 - Merged Preliminary Offering Document.pdf
> - Time taken: 326.90 seconds (5+ minutes)
> - Total fields: 29; extracted: 29; pending: 0
> Summary: issue is doc 3 can take very long, may break for some requests. Changed logic to extract/store per document and update when new fields extracted.

## 09:50 - Navsheen Koul
> these were my notes from friday on testing. tbh the system was crashing bad so weren't able to test the large PDfs

# Teams Chat — LCP Finance Doc Extraction Handover

## 09:50 - Navsheen Koul
> these were my notes from friday on testing. tbh the system was crashing bad so weren't able to test the large PDfs
> <attachment id="1770392585584"></attachment>

## 09:42 - Ajay Gannamaneni
> Breakdown:
> Document 1: Email_2026-02-06.pdf
> - Time Taken for Analysis: Started 2026-02-06 11:21:56, Completed 2026-02-06 11:22:08 (9.45 seconds)
> - Fields Extracted: Total 29, Extracted 7, Pending 22; confidence issue: MaturityDate not confident enough.
> Document 2: Lion Re DAC 2025-1 Investor Presentation.pdf
> - Started 2026-02-06 11:22:21, Completed 2026-02-06 11:22:50 (25.02 seconds)
> - Fields Extracted: Total 29, Extracted 7, Pending 22; confidence issue: MaturityDate.
> Document 3: Lion Re DAC - Series 2025-1 - Merged Preliminary Offering Document.pdf
> - Started 2026-02-06 11:23:04, Completed 2026-02-06 11:28:40 (326.90 seconds)
> - Fields Extracted: Total 29, Extracted 29, Pending 0; varying confidence.
> Summary: doc 3 sometimes takes very long so may break; changed logic to extract/store per document and update as new fields are extracted.

## 09:39 - Navsheen Koul
> Sheet to add bugs - https://synapxltd-my.sharepoint.com/:x:/g/personal/ajay_gannamaneni_synapx_com/IQDbrR2pZFK3TpNUdEWRLqqEAfqoGdWUDxWc7xSipgcaT-o?e=6oG9b7 (LCP_updated.xlsx)
> <attachment id="A91DADDB-5264-4EB7-9354-7445912EAA84"></attachment>

## 09:38 - Navsheen Koul
> <attachment id="218111a8-0c17-4056-96e7-ff5725bf9d9a"></attachment>

## 09:30 - Unknown
> <systemEventMessage/>

# Teams Chat — LCP Finance Doc Extraction Handover

## 10:25 - Ajay Gannamaneni
> we extract the different fields and create a temporary pdf

## 10:24 - Timon Wan
> @Ajay @Gannamaneni how does the plugin convert the outlook email to a PDF?

## 10:22 - Timon Wan
> cheers

## 10:22 - Navsheen Koul
> i have forwarded you the emails - look for outlook attachment type

## 10:21 - Timon Wan
> @Navsheen @Koul/@Ajay @Gannamaneni can you send across the PDFs of the emails please.
> Or point me to where they are


# Teams Chat — LCP Finance Doc Extraction Handover

## 10:27 - Ajay Gannamaneni
> ignore above i will send again

## 10:27 - Timon Wan
> thanks

## 10:27 - Ajay Gannamaneni
> 

## 10:26 - Timon Wan
> That PDF is then saved somewhere or not

## 10:25 - Ajay Gannamaneni
> we extract the different fields and create a temporary pdf

## 10:24 - Timon Wan
> @Ajay @Gannamaneni how does the plugin convert the outlook email to a PDF?

## 10:22 - Timon Wan
> cheers

## 10:22 - Navsheen Koul
> <attachment id="1770718867032"></attachment>
> i have forwarded you the emails - look for outlook attachment type

## 10:21 - Timon Wan
> @Navsheen @Koul/@Ajay @Gannamaneni can you send across the PDFs of the emails please.
> Or point me to where they are



## 10:40 - Timon Wan
> <p>thanks</p>

## 10:38 - Ajay Gannamaneni
> <attachment id="535ee06e-af5b-4f8d-b52d-4617bdc9078f"></attachment><attachment id="9ecd2cfc-9f80-4558-986b-2be8d308c8d3"></attachment>

## 10:27 - Ajay Gannamaneni
> <p>ignore above i will send again</p>

## 10:27 - Timon Wan
> <p>thanks</p>

## 10:27 - Ajay Gannamaneni
> 

## 10:26 - Timon Wan
> <p>That PDF is then saved somewhere or not</p>

## 10:25 - Ajay Gannamaneni
> <p>we extract the different fields and create a temporary pdf</p>

## 10:24 - Timon Wan
> <p><at id="0">Ajay</at>&nbsp;<at id="1">Gannamaneni</at>&nbsp;how does the plugin convert the outlook email to a PDF?</p>

## 10:22 - Timon Wan
> <p>cheers</p>

## 10:22 - Navsheen Koul
> <attachment id="1770718867032"></attachment>
> <p>i have forwarded you the emails - look for outlook attachment type&nbsp;</p>
