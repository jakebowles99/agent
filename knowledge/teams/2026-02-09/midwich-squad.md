# Teams Chat — Midwich Squad (chat_id: 19:438220475ac84c8e92ef0a36e2ae8b0a@thread.v2)

## 16:20 - Unknown
> Tim any chance you could check connection references etc. is it pointing to DEV dB?
> (attachment id: 1770653976814)

## 16:21 - Timon Wan
> sure

## 16:23 - Unknown
> This is what Umar is seeing when he opens it
> (attachment id: 1770653967302)

## 16:24 - Timon Wan
> i'll connect with him directly

## 16:32 - Yaz Qaraqesh
> Amazing thanks pal

## 16:33 - Timon Wan
> Are we still using db-orders-1 btw?

## 16:44 - Yaz Qaraqesh
> I'd wait for Hemanth / Vaishnavi to confirm tomorrow

## 16:44 - Yaz Qaraqesh
> (attachment id: 1770654273548)
> Is the issue sorted?

## 16:45 - Timon Wan
> He's away atm
> but when I open the app, it's pointing to UAT (old db hence my q above)



## 16:45 - Timon Wan
> ah wait, for that new part I do see the same error

## 16:45 - Nandan Hegde
> UAT database is the db-orders-1

## 16:45 - Timon Wan
> He's back now, so will jump on a call with him

## 16:46 - Timon Wan
> Thanks for confirming

## 16:50 - Timon Wan
> Vaishnavi MP
>
> For tomorrow, can you just rename the display name of env var: 'synapx_ev_OrderManagementPOsqlDatabase' to 'ev_OrderManagementPOsqlDatabase'. ID of the env var is correct, but just trim the Display name.


## 18:39 - Timon Wan
> @Vaishnavi @MP for tomorrow, can you check Umar's PO app in UAT if it's using env vars for the data sources? Specifically the bid reference.

## 18:43 - Yaz Qaraqesh
> Is the issue resolved please Tim?

## 18:43 - Yaz Qaraqesh
> Temporarily

## 18:45 - Timon Wan
> No, I'm getting issues when trying to edit the App to view what datasources there are
> Best thing is tomorrow Vaishnavi to work with Umar on it
