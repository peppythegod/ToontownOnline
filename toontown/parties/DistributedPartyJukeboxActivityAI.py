from direct.directnotify import DirectNotifyGlobal
from toontown.parties.DistributedPartyJukeboxActivityBaseAI import DistributedPartyJukeboxActivityBaseAI


class DistributedPartyJukeboxActivityAI(DistributedPartyJukeboxActivityBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        "DistributedPartyJukeboxActivityAI")
