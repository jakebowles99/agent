# Product Catchup

Meeting chat for LCP document extraction product development (Navsheen Koul, Rahul Matta, Jake Bowles).

## 05:41 - Navsheen Koul
> morning Rahul
>
> the steps will be needs review > in review > approved/rejected
>
> the reason i want to add in review is that when a claim is being investigated by an analyst then another analyst should be able to see so that they dont pick up the same claim which is already being worked at by someone else. hope that makes sense.

## 05:42 - Navsheen Koul
> what do you mean by status badge exactly, please share a a screenshot

## 05:43 - Navsheen Koul
> dont touch 'needs review', never said replace. add 'in review'

## 06:23 - Rahul Matta
> Good Morning Navsheen
>
> Understood, will add "in review"

## 06:46 - Rahul Matta
> Hi @Navsheen,
>
> One small doubt
>
> When a user puts a claim into "In Review", it'll be logged as that specific user did that.
> Should we then restrict approve/reject to the same user, or allow anyone to do it?
> Asking since it may look odd if different people handle different steps.

## 06:48 - Navsheen Koul
> good question and this will need to be considered with more feedback from LCP if they go ahead with it as to how do they handle these workflows in their business

## 06:48 - Navsheen Koul
> for now anybody can do whatever for demo purposes, not priority for now

## 06:48 - Rahul Matta
> got it, thanks

---

**Context:** This relates to the LCP Document Extraction product. Navsheen is clarifying the claim review workflow states to Rahul:
- `Needs Review` - claim awaiting analyst attention
- `In Review` (NEW) - claim being actively worked by an analyst (prevents duplicate work)
- `Approved` / `Rejected` - final states

The "In Review" status is being added to prevent multiple analysts picking up the same claim simultaneously.
