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

# Teams Chat — Midwich Squad

## 12:19 - Vaishnavi MP
> Seen another issue in Prod. Some tables reference the dev db. I think we might have to switch back to readding tables and creating an unmanaged layer for now? Until we replace all direct references to tables with stored procedures

## 12:12 - Hemanth Kotha
> If that's the case then I don't see a big use of PA and Log Analytics integration. Mostly we need live monitor logs to be streamed as we use it for debugging mostly. And one more thing that I have observed is power apps is using whole pp subnet for calling SQL every time it uses a different ip. Not sure how it works.

## 12:04 - Timon Wan
> Yes will need KQL, million dollar question is atm what ootb logs can Power Apps give.
> 
> I've not see a way to connect Live Monitoring to stream to App Insights/Log Analytics
> 
> From what I read it's more high level telemetry, so anything useful to us might need to be using Trace to log custom events. FYI Vaishnavi MP




## 12:33 - Vaishnavi MP
> The PO app uses many tables to get or add data. Can give an estimate to switch to sprocs. I suggest we do this as a part of next big change i.e. when we implement the approval process

# Teams Chat — Midwich Squad

## 13:00 - Yaz Qaraqesh
> Can SO app wait?

## 13:00 - Timon Wan
> Reminder that SO App link with change following this deployment as we'll do a fresh install in prod of everything.

## 12:59 - Yaz Qaraqesh
> V, Tim, Hemanth please coordinate together. I can sense check when ready. 
> 
> You could do this by tomorrow AM UK time please

## 12:58 - Yaz Qaraqesh
> Can this work commence ASAP - if you're part of this work, drop everything else please

## 12:58 - Yaz Qaraqesh
> @Everyone I have approval from Midwich to promote PO app from UAT to production

## 12:57 - Timon Wan
> Thanks

## 12:57 - Vaishnavi MP
> Sure. Will let you know when done

## 12:56 - Timon Wan
> Can you add a few Trace statements in the dev SO app for when you call the sprocs/flows/SharePoint please.
> No need to go overboard now, but I want to see what the logs look like going into Azure

## 12:54 - Timon Wan
> Yes, let's not make any changes right now. Just understanding what needs to be done and how complex it would be.


# Teams Chat — Midwich Squad

## 13:13 - Yaz Qaraqesh
> SO APP users need to be the same on PROD
> 
> PO APP ACCESS shown in this list:
> 
> https://synapxltd.sharepoint.com.mcas.ms/:x:/r/sites/SynapxMidwich-SOW001/_layouts/15/Doc2.aspx?act…
> 
> Need V to manage please

## 13:09 - Timon Wan
> Cautious me would say tomorrow IST time when there's no active users.

## 13:09 - Yaz Qaraqesh
> hold fire guys I'll try to get SO app signoff shortly

## 13:08 - Hemanth Kotha
> I have added few additional indexes for optimization

## 13:07 - Hemanth Kotha
> Impacts will be on sync.

## 13:05 - Timon Wan
> [attachment]
> How long and what impacts will it have?

## 13:05 - Hemanth Kotha
> Should I start db deployment now to prod or everything starts to morning. I need to manually deploy few scripts so mine will take time

## 13:03 - Yaz Qaraqesh
> Then all can happen together nicely

## 13:03 - Yaz Qaraqesh
> Beautiful. Please await my confirmation on SO app

## 13:03 - Vaishnavi MP
> Sure will do. Once complete I can share the links with you
> Yaz Qaraqesh the Network issue that they see should be resolved after tomorrow's push

# Teams Chat — Midwich Squad

## 13:17 - Yaz Qaraqesh
> <attachment id="1770815833763"></attachment>
> yes boss

## 13:17 - Yaz Qaraqesh
> <attachment id="1770815818935"></attachment>
> Is that for me

## 13:17 - Timon Wan
> <attachment id="1770815833763"></attachment>
> Thanks for reminder 🙂

## 13:17 - Jake Bowles
> threads please

## 13:16 - Timon Wan
> Can you note down here what versions of each Solution is in UAT atm please.
> Those will be what we'll deploy and nothing should go into UAT today.

## 13:16 - Yaz Qaraqesh
> any ground work that can happen now please go ahead with team

## 13:15 - Timon Wan
> Thanks

## 13:15 - Vaishnavi MP
> @Timon Wan going to update the checklist and Environment variable list for tomorrow's deployment

## 13:13 - Yaz Qaraqesh
> SO APP users need to be the same on PROD
> 
> PO APP ACCESS shown in this list:
> 
> https://synapxltd.sharepoint.com.mcas.ms/:x:/r/sites/SynapxMidwich-SOW001/_layouts/15/Doc2.aspx?act…
> 
> Need V to manage please

## 13:09 - Timon Wan
> Cautious me would say tomorrow IST time when there's no active users.

# Teams Chat — Midwich Squad

## 14:09 - Yaz Qaraqesh
> Please proceed

## 14:09 - Yaz Qaraqesh
> @Everyone approval to deploy both SO & PO to prod

# Teams Chat — Midwich Squad

## 14:09 - Yaz Qaraqesh
> Everyone approval to deploy both SO & PO to prod

## 14:09 - Yaz Qaraqesh
> Please proceed

## 14:30 - Hemanth Kotha
> Yaz Qaraqesh I don't have access to the security users list


# Teams Chat — Midwich Squad

## 14:30 - Hemanth Kotha
> Yaz Qaraqesh I don't have access to the security users list

## 14:30 - Hemanth Kotha
> It should also need to include the role as well.

## 14:33 - Yaz Qaraqesh
> try again please

## 14:34 - Hemanth Kotha
> Now works. Thanks

## 14:35 - Hemanth Kotha
> What do you mean by General?

## 14:36 - Vaishnavi MP
> I need same permissions please

## 14:36 - Yaz Qaraqesh
> Anything works for those - do we have an "Admin" role?

## 14:37 - Hemanth Kotha
> They can't override the approval process.

## 14:37 - Hemanth Kotha
> If they need to approve or create they need to have multiple roles

## 14:40 - Hemanth Kotha
> (100000, 'Product Manager / Brand Manager', 100000),
> (100001, 'Purchaser', 100000),
> (100002, 'Warehouse Manager', 100000),
> (100003, 'Business Administrator / System Administrator', 100000),
> (100004, 'Finance', 100000),
> (100005, 'Accounts Payable', 100000),
> (100006, 'Business Manager', 100000),
> (100007, 'Supply Chain Manager', 100000),
> (100008, 'Director BM / Commercial Director', 100000),
> (100009, 'CFO / MD', 100000),
> (100010, 'Client / Customer', 100000),
> (100011, 'Sales Support / Administration', 100000),
> (100012, 'Sales Manager / Account Manager', 100000),
> (100013, 'Sales Director', 100000),
> (100014, 'App Admin', 100000),
> (100015, 'Sales Admin', 100000),
> (100016, 'Sales Standard', 100000),
> (100017, 'Product Manager / Brand Manager', 100001),
> (100018, 'Purchaser', 100001),
> (100019, 'Warehouse Manager', 100001),
> (100020, 'Business Administrator / System Administrator', 100001),
> (100021, 'Finance', 100001),
> (100022, 'Accounts Payable', 100001),
> (100023, 'Business Manager', 100001),
> (100024, 'Supply Chain Manager', 100001),
> (100025, 'Director BM / Commercial Director', 100001),
> (100026, 'CFO / MD', 100001),
> (100027, 'Client / Customer', 100001),
> (100028, 'Sales Support / Administration', 100001),
> (100029, 'Sales Manager / Account Manager', 100001),
> (100030, 'Sales Director', 100001);

