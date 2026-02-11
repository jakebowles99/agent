# Teams Chat — Prathap Reddy

## 05:57 - Prathap Reddy
> Hi Jake Bowles, Good evening.
> 
> - Completed the Word template setup with all required content controls (company details plus Background, Scope, Deliverables, Out of Scope, Rate Card, Fees & Agreement) so Logic Apps can populate every section dynamically.
> - Updated and aligned the HTTP trigger schema and OpenAPI `SOWInput` model to support all SOW fields and multiple uploaded files, and started wiring those fields into the Logic App’s “Populate a Microsoft Word template” action for end‑to‑end SOW generation.


# Teams Chat — Prathap Reddy

## 06:01 - Prathap Reddy
> Sorry, it was drafted in your personal chat. I’ve just sent it please check. Thank you.

## 05:57 - Prathap Reddy
> Hi @Jake @Bowles, Good evening. 
> 
> - Completed the Word template setup with all required content controls (company details plus Background, Scope, Deliverables, Out of Scope, Rate Card, Fees & Agreement) so Logic Apps can populate every section dynamically.  
> - Updated and aligned the HTTP trigger schema and OpenAPI `SOWInput` model to support all SOW fields and multiple uploaded files, and started wiring those fields into the Logic App’s “Populate a Microsoft Word template” action for end‑to‑end SOW generation.


## 06:01 - Prathap Reddy
> Sorry, it was drafted in your personal chat. I’ve just sent it please check. Thank you.

# Teams Chat — Prathap Reddy

## 05:57 - Prathap Reddy
> Hi Jake Bowles, Good evening.
> - Completed the Word template setup with all required content controls (company details plus Background, Scope, Deliverables, Out of Scope, Rate Card, Fees & Agreement) so Logic Apps can populate every section dynamically.
> - Updated and aligned the HTTP trigger schema and OpenAPI `SOWInput` model to support all SOW fields and multiple uploaded files, and started wiring those fields into the Logic App’s “Populate a Microsoft Word template” action for end‑to‑end SOW generation.

## 06:01 - Prathap Reddy
> Sorry, it was drafted in your personal chat. I’ve just sent it please check. Thank you.


# Teams Chat — Prathap Reddy

## 16:00 - Prathap Reddy
>  I built the Logic App end-to-end to handle multiple documents by looping through files. extracting full text from each file using Azure AI (prebuilt-read), merging it into a single CombinedText, and then calling Azure OpenAI (sow-extractor deployment) to generate the required 17 SOW fields JSON, which is mapped into the Word template to produce the final SOW and return a share link and also identified a Teams/agent chat platform limitation where some file types EX .docx are blocked by the attachment/context allow-list before the flow runs, so the enterprise-ready approach for Teams is to use SharePoint/Teams Files as the upload source and have the agent trigger the same DI, OpenAI,Word pipeline from that folder. Tomorrow i'm deploying into teams and i'll show the demo meanwhile i will work on the progress.

# Teams Chat — Prathap Reddy

## 16:00 - Prathap Reddy
>  I built the Logic App end-to-end to handle multiple documents by looping through files. extracting full text from each file using Azure AI (prebuilt-read), merging it into a single CombinedText, and then calling Azure OpenAI (sow-extractor deployment) to generate the required 17 SOW fields JSON, which is mapped into the Word template to produce the final SOW and return a share link and also identified a Teams/agent chat platform limitation where some file types EX .docx are blocked by the attachment/context allow-list before the flow runs, so the enterprise-ready approach for Teams is to use SharePoint/Teams Files as the upload source and have the agent trigger the same DI, OpenAI,Word pipeline from that folder. Tomorrow i'm deploying into teams and i'll show the demo meanwhile i will work on the progress.
