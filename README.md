# Commonman Playbooks

*Working name. The real name will come later. Until then the site lives at satsangee.org.*

Money has left your account and you did not send it. Or someone in a police uniform is on a video call, telling you that you are under arrest. The first thing anyone asks at that moment is "what do I do now?", and India has no single place that answers it. The 1930 helpline and cybercrime.gov.in take your complaint. They do not tell you what to do first, or where to go when the bank stops replying.

This project writes those answers down. One page for each thing that goes wrong, in English, Odia and Hindi, meant to be read on a cheap phone by someone who is frightened. Each page will also come as a WhatsApp message and a one-page print sheet, built from the same checked facts, so the three can never disagree.

## Status

Nothing is live yet. This repo has the plan, the house rules, the scam families and the page templates. The first page will be "Money left my account and I didn't send it".

## How a page is made

AI does a lot of the work here. It checks police and I4C advisories every day for new scams, and it writes the first draft of each page from the official sources. A second AI, from a different company, then checks every claim in that draft against the same sources.

After that I read the sources myself and decide. I can reject a draft as many times as it takes. Nothing goes live until I sign it, and every page shows the date I signed it.

Every phone number and link on the site comes from one list, checked by hand against the owner's own website. If a page carries a number that is not on that list, the build fails. Scammers plant fake helpline numbers everywhere, so this rule does not bend.

The rules every page follows are in [rules/house-rules.md](rules/house-rules.md).

## What the site will never do

It will never call you, message you, ask for money or ask for your details. It will never file a complaint for you. Anyone who says they are from this site and asks for any of that is running a scam. Report them at cybercrime.gov.in or on 1930.

## Found a mistake?

Open an issue with the "Wrong fact on a page" template. Please leave out phone numbers, account numbers and anything else personal, because this repo will be public.

## Who

Satyasai Ray. I have spent 14 years in security operations: SOC work, detection engineering, data loss prevention, and a lot of playbooks and SOPs. The pages here follow the same incident-response habits. Contain the damage first, keep the evidence, escalate in order, and write down what failed.

This is a non-profit project. It takes no money and carries no ads.

## Licence

Not decided yet.
