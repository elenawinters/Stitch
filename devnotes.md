# Stitch Devnotes

If you found these, I accidently included them in a push somehow. Anyways. I always create these kinds of files

## Thread Communications Manager

This will likely be added to the thread manager in general which will talk to the MAIN file `berry.py`

Will use queue's

Thread pool has a pool of queue's unique to each thread. If a thread wants to say smth, it does

Manager will respond to the thread if it needs to

Manager can broadcast messages from one thread to all

MAIN can also broadcast thru manager if it needs to.

MAIN is the heart of the operation

All modules need to be able to process the queue async and respond to things at any time. This might be tricky with asyncio and discord.py


MAIN <-> MANAGER <-> ANY THREAD

Manager needs to be sophisticated to handle everything. Main should inherit from Manager potentially so that it can add it's own things.

## Database

This ideally should use the communication network and take raw SQL strings as data.
We want this to be SYNC, because dataset and sqlite be like pfvrafjkahsdf
