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
