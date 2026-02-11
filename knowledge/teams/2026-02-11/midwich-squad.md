# Teams Chat — Midwich Squad

## 10:00 - Hemanth Kotha
> <ol>
<li>ResultSets: {Table1: [,26], Table2: [{TotalCount: 4076}]}
<ol>
<li>Table1: [,26]</li><li>Table2: [{TotalCount: 4076}]
<ol>
<li>0: {TotalCount: 4076}
<ol>
<li>TotalCount: 4076</li></ol>
</li></ol>
</li></ol>
</li></ol>

## 09:59 - Hemanth Kotha
> 

## 09:57 - Dhanush Pamarthi
> <attachment id="1770803431426"></attachment>
<p>Working on that, will let you know if it works from app side.&nbsp;</p>

## 09:50 - Hemanth Kotha
> <attachment id="1770803366959"></attachment>
<p>I would not call it as workaround specifically but that's how we need to use it on App side for dynamic results from sql sproc side</p>

## 09:49 - Timon Wan
> <p>Is this the only work around?</p>
<p>Concerned about behaviour of the Apps post deployment and ow stable that would be</p>

## 09:48 - Yaz Qaraqesh
> <p><at id="0">Vaishnavi</at>&nbsp;<at id="1">MP</at>&nbsp;can you assist Dhanush with a high priority please. The new approval flow needs to be shipped ASAP</p>

## 09:48 - Hemanth Kotha
> <p>If the above workaround works we can remove lot of unwanted temp tables and table variables in sql side</p>

## 09:47 - Hemanth Kotha
> <attachment id="1770803155364"></attachment>
<p>Hey Yaz. I'm not Apps pro / specialist. But can someone from Apps help him based on the above link.</p>

## 09:45 - Yaz Qaraqesh
> <p><at id="0">Dhanush</at>&nbsp;<at id="1">Pamarthi</at>&nbsp;did you meet with Hemanth? is the issue resolved?&nbsp;</p>

# Teams Chat — Midwich Squad

## 10:31 - Hemanth Kotha
> Can you check the api call what it passed?

## 10:29 - Vaishnavi MP
> Order date is being passed as the current date on the app side

## 10:29 - Yaz Qaraqesh
> @Vaishnavi @MP how is this possible please. Created date is when the order is created

## 10:27 - Hemanth Kotha
> There is no validation on sql side for taking dates it should come from the app if we don't get it from app then sql automatically assign todays date

## 10:24 - Hemanth Kotha
> That's what user passed from app side

## 10:22 - Yaz Qaraqesh
> @Vaishnavi @MP @Hemanth @Kotha how is it possible to have date created in the future
> 
> Can someone check this order asap please on the PO app in UAT
> 
> 100120

## 10:19 - Yaz Qaraqesh
> same with @Vaishnavi @MP - does Ella have the correct permissions on PO app

## 10:19 - Yaz Qaraqesh
> can @Hemanth @Kotha confirm Ella's permission on the PO app?

## 10:18 - Dhanush Pamarthi
> Nope.


# Teams Chat — Midwich Squad

## 10:33 - Yaz Qaraqesh
> https://dev.azure.com/mw-synapx/SlipStream/_workitems/edit/226
> 
> Ticket for resolving this please. Assigned to V

## 10:32 - Hemanth Kotha
> This shouldn't happen if both tools has GETDATE() TODAY()

## 10:31 - Vaishnavi MP
> Yes doing that now in UAT

## 10:31 - Hemanth Kotha
> [attachment]
> Can you check the api call what it passed?

## 10:29 - Vaishnavi MP
> [image]
> 
> Order date is being passed as the current date on the app side

## 10:29 - Yaz Qaraqesh
> @Vaishnavi @MP how is this possible please. Created date is when the order is created

## 10:27 - Hemanth Kotha
> There is no validation on sql side for taking dates it should come from the app if we don't get it from app then sql automatically assign todays date

## 10:24 - Hemanth Kotha
> [image]
> 
> That's what user passed from app side

## 10:22 - Yaz Qaraqesh
> @Vaishnavi @MP @Hemanth @Kotha how is it possible to have date created in the future
> 
> [image]
> 
> Can someone check this order asap please on the PO app in UAT
> 
> 100120

## 10:22 - Hemanth Kotha
> [image]

# Teams Chat — Midwich Squad

## 11:16 - Yaz Qaraqesh
> <attachment id="1770807901516"></attachment>
> What's the conclusion on this guys please?

## 11:13 - Hemanth Kotha
> @Timon I have validated all the sql servers have connected audits to their env specific log analytics ws. Do I also need to deploy application insights for sql as well?

## 11:08 - Hemanth Kotha
> Can you check the one for the above record. Not new one.

## 11:05 - Vaishnavi MP
> Just created a record on UAT. Here's the api call
> 
> [image]
> 
> Get's the right date


## 11:27 - Timon Wan
> [attachment]
> 
> Thanks, re. App Insights, don't think so. May be useful to trace from app to db, but not sure that would work ootb. Your thoughts?

# Teams Chat — Midwich Squad

## 11:37 - Hemanth Kotha
> <attachment id="1770809224016"></attachment>
> We might tneed to create a kql that links both app and sql db for better classification for app insights and also can have alerts since any way it's configured for apps ide

## 11:36 - Hemanth Kotha
> retention was set to 30 days. I can't see the logs on sql side as well since the record was inserted on

## 11:27 - Timon Wan
> Thanks, re. App Insights, don't think so. May be useful to trace from app to db, but not sure that would work ootb. Your thoughts?

## 11:16 - Yaz Qaraqesh
> What's the conclusion on this guys please?

## 11:13 - Hemanth Kotha
> @Timon I have validated all the sql servers have connected audits to their env specific log analytics ws. Do I also need to deploy application insights for sql as well?

## 11:08 - Hemanth Kotha
> Can you check the one for the above record. Not new one.

## 11:05 - Vaishnavi MP
> Just created a record on UAT. Here's the api call
> Get's the right date

# Teams Chat — Midwich Squad

## 12:12 - Hemanth Kotha
> <attachment id="1770811463164"></attachment>
> <p>If that's the case then I don't see a big use of PA and Log Analytics integration. Mostly we need live monitor logs to be streamed as we use it for debugging mostly. And one more thing that I have observed is power apps is using whole pp subnet for calling SQL every time it uses a different ip. Not sure how it works.&nbsp;</p>

## 12:04 - Timon Wan
> <attachment id="1770809861480"></attachment>
> <p>Yes will need KQL, million dollar question is atm what ootb logs can Power Apps give.&nbsp;</p>
> <p>I've not see a way to connect Live Monitoring to stream to App Insights/Log Analytics</p>
> <p>From what I read it's more high level telemetry, so anything useful to us might need to be using Trace to log custom events. FYI&nbsp;<at id="0">Vaishnavi</at>&nbsp;<at id="1">MP</at></p>
> <p>&nbsp;</p>
> <p>&nbsp;</p>
