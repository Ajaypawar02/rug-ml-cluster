# rug-ml-cluster

### Installation

You can install the requirements using the command `pip install -r requirements.txt` in the root directory.

### Task

In the directory `data` there is a file `data/interactions.json` which contains random interactions between users of a network. This data is randomly generated according to the script `utils/generate_graph.py`.

This data contains interactions between users denoted by IDs `user0` and `user1`, where in each interaction `user0` is sending `user1` an asset of a specific lettered type, in some quantity and at some specific time.

Assume that the current time is `19,000,000`, such that all interactions occurred in the past.

**Problem:** Given this information, the task is to determine which users hold token `A` which was created at some point after time `16,000,000`. 

**Notes:** Different user IDs can correspond to the same person controlling different IDs. You should assume that if IDs interacted with eachother prior to holding token `A`, that these user IDs are the same person. In this case, output a list of user IDs which correspond to an ID cluster and the same underlying user also. You can consider this a problem of clustering a social graph of holders of token `A`.

In addition, ensure to take care of the computational complexity and runtime of your solution. Solutions which work for varying depth of interaction and output information visually will be highly sought.
