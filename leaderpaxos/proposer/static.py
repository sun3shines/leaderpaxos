
PAXOS_LEADER_TERM = 30

ACCEPTOR_LEARN_INTERVAL = PAXOS_LEADER_TERM/10

PRINCE_TERM = LEADER_TERM/4


PAXOS_HOST_TERM = 30

PAXOS_HOST_COUNT = 100

PAXOS_HOST_BASE = 1

PAXOS_HOST_ROUND = 0

PAXOS_HOST_LEARN = PAXOS_HOST_TERM/10

# 学习hostUuid，并学习任期的剩余时间了。
# acceptor启动的第一件事情，就是学习了。
# 避免出现学习到了两个值了。是的。

# 为了快速的解决抢占，还是用编号吧。promise编号的方式了。
# 首先是学习阶段了，如果大家都没有，那就好办了。是的。如果在学习阶段，大家都没有学习到怎么？学习完了所有的主机了 
# 先写把，不要陷入完美主义陷阱中了。
