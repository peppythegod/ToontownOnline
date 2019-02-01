from direct.directnotify.DirectNotifyGlobal import *
from direct.gui.DirectGui import *
from direct.showbase import DirectObject, PythonUtil
from pandac.PandaModules import *
from toontown.parties import PartyGlobals
from toontown.parties.InviteInfo import InviteInfoBase
from toontown.parties.PartyGlobals import InviteStatus
from toontown.parties.SimpleMailBase import SimpleMailBase
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui import TTDialog
from toontown.toontowngui.TeaserPanel import TeaserPanel
from toontown.parties.InviteVisual import InviteVisual
import CatalogItem
from direct.showbase.PythonUtil import StackTrace


class MailboxScreen(DirectObject.DirectObject):
    notify = directNotify.newCategory('MailboxScreen')

    def __init__(self, mailbox, avatar, doneEvent=None):
        self.mailbox = mailbox
        self.avatar = avatar
        self.items = self.getItems()
        self.doneEvent = doneEvent
        self.itemIndex = 0
        self.itemPanel = None
        self.itemPicture = None
        self.ival = None
        self.itemText = None
        self.giftTag = None
        self.acceptingIndex = None
        self.numAtticAccepted = 0
        self.dialogBox = None
        self.load()
        self.hide()

    def show(self):
        self.frame.show()
        self._MailboxScreen__showCurrentItem()

    def hide(self):
        self.ignore('friendsListChanged')
        if hasattr(self, 'frame'):
            self.frame.hide()
        else:
            self.notify.warning(
                'hide called, but frame is deleted, self.frame deleted in:')
            if hasattr(self, 'frameDelStackTrace'):
                print self.frameDelStackTrace

            self.notify.warning('current stackTrace =')
            print StackTrace()
            self.notify.warning('crash averted, but root cause unknown')

    def load(self):
        self.accept(
            'setMailboxContents-%s' %
            base.localAvatar.doId,
            self._MailboxScreen__refreshItems)
        self.accept(
            'setAwardMailboxContents-%s' %
            base.localAvatar.doId,
            self._MailboxScreen__refreshItems)
        model = loader.loadModel('phase_5.5/models/gui/package_delivery_panel')
        background = model.find('**/bg')
        itemBoard = model.find('**/item_board')
        self.frame = DirectFrame(
            scale=1.1000000000000001, relief=DGG.FLAT, frameSize=(
                -0.5, 0.5, -0.45000000000000001, -0.050000000000000003), frameColor=(
                0.73699999999999999, 0.57299999999999995, 0.34499999999999997, 1.0))
        self.background = DirectFrame(
            self.frame,
            image=background,
            image_scale=0.050000000000000003,
            relief=None,
            pos=(
                0,
                1,
                0))
        self.itemBoard = DirectFrame(
            parent=self.frame,
            image=itemBoard,
            image_scale=0.050000000000000003,
            image_color=(
                0.92200000000000004,
                0.92200000000000004,
                0.753,
                1),
            relief=None,
            pos=(
                0,
                1,
                0))
        self.itemCountLabel = DirectLabel(
            parent=self.frame,
            relief=None,
            text=self._MailboxScreen__getNumberOfItemsText(),
            text_wordwrap=16,
            pos=(
                0.0,
                0.0,
                0.69999999999999996),
            scale=0.089999999999999997)
        exitUp = model.find('**/bu_return_rollover')
        exitDown = model.find('**/bu_return_rollover')
        exitRollover = model.find('**/bu_return_rollover')
        exitUp.setP(-90)
        exitDown.setP(-90)
        exitRollover.setP(-90)
        self.DiscardButton = DirectButton(
            parent=self.frame, relief=None, image=(
                exitUp, exitDown, exitRollover, exitUp), pos=(
                -0.01, 1.0, -0.35999999999999999), scale=0.048000000000000001, text=(
                '', TTLocalizer.MailBoxDiscard, TTLocalizer.MailBoxDiscard, ''), text_scale=1.0, text_pos=(
                    0, -0.080000000000000002), textMayChange=1, command=self._MailboxScreen__makeDiscardInterface)
        gui2 = loader.loadModel('phase_3/models/gui/quit_button')
        self.quitButton = DirectButton(
            parent=self.frame,
            relief=None,
            image=(
                gui2.find('**/QuitBtn_UP'),
                gui2.find('**/QuitBtn_DN'),
                gui2.find('**/QuitBtn_RLVR')),
            pos=(
                0.5,
                1.0,
                -0.41999999999999998),
            scale=0.90000000000000002,
            text=TTLocalizer.MailboxExitButton,
            text_font=ToontownGlobals.getSignFont(),
            text0_fg=(
                0.152,
                0.75,
                0.25800000000000001,
                1),
            text1_fg=(
                0.152,
                0.75,
                0.25800000000000001,
                1),
            text2_fg=(
                0.97699999999999998,
                0.81599999999999995,
                0.13300000000000001,
                1),
            text_scale=0.044999999999999998,
            text_pos=(
                0,
                -0.01),
            command=self._MailboxScreen__handleExit)
        self.gettingText = DirectLabel(
            parent=self.frame, relief=None, text='', text_wordwrap=10, pos=(
                0.0, 0.0, 0.32000000000000001), scale=0.089999999999999997)
        self.gettingText.hide()
        self.giftTagPanel = DirectLabel(
            parent=self.frame,
            relief=None,
            text='Gift TAG!!',
            text_wordwrap=16,
            pos=(
                0.0,
                0.0,
                0.01),
            scale=0.059999999999999998)
        self.giftTagPanel.hide()
        self.itemText = DirectLabel(
            parent=self.frame, relief=None, text='', text_wordwrap=16, pos=(
                0.0, 0.0, -0.021999999999999999), scale=0.070000000000000007)
        self.itemText.hide()
        acceptUp = model.find('**/bu_check_up')
        acceptDown = model.find('**/bu_check_down')
        acceptRollover = model.find('**/bu_check_rollover')
        acceptUp.setP(-90)
        acceptDown.setP(-90)
        acceptRollover.setP(-90)
        self.acceptButton = DirectButton(
            parent=self.frame, relief=None, image=(
                acceptUp, acceptDown, acceptRollover, acceptUp), image3_color=(
                0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 0.59999999999999998), pos=(
                -0.01, 1.0, -0.16), scale=0.048000000000000001, text=(
                    '', TTLocalizer.MailboxAcceptButton, TTLocalizer.MailboxAcceptButton, ''), text_scale=1.0, text_pos=(
                        0, -0.089999999999999997), textMayChange=1, command=self._MailboxScreen__handleAccept, state=DGG.DISABLED)
        nextUp = model.find('**/bu_next_up')
        nextUp.setP(-90)
        nextDown = model.find('**/bu_next_down')
        nextDown.setP(-90)
        nextRollover = model.find('**/bu_next_rollover')
        nextRollover.setP(-90)
        self.nextButton = DirectButton(
            parent=self.frame,
            relief=None,
            image=(
                nextUp,
                nextDown,
                nextRollover,
                nextUp),
            image3_color=(
                0.80000000000000004,
                0.80000000000000004,
                0.80000000000000004,
                0.59999999999999998),
            pos=(
                0.31,
                1.0,
                -0.26000000000000001),
            scale=0.050000000000000003,
            text=(
                '',
                TTLocalizer.MailboxItemNext,
                TTLocalizer.MailboxItemNext,
                ''),
            text_scale=1,
            text_pos=(
                -0.20000000000000001,
                0.29999999999999999),
            text_fg=(
                1,
                1,
                1,
                1),
            text_shadow=(
                0,
                0,
                0,
                1),
            textMayChange=0,
            command=self._MailboxScreen__nextItem,
            state=DGG.DISABLED)
        prevUp = model.find('**/bu_previous_up')
        prevUp.setP(-90)
        prevDown = model.find('**/bu_previous_down')
        prevDown.setP(-90)
        prevRollover = model.find('**/bu_previous_rollover')
        prevRollover.setP(-90)
        self.prevButton = DirectButton(
            parent=self.frame, relief=None, image=(
                prevUp, prevDown, prevRollover, prevUp), pos=(
                -0.34999999999999998, 1, -0.26000000000000001), scale=0.050000000000000003, image3_color=(
                0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 0.59999999999999998), text=(
                    '', TTLocalizer.MailboxItemPrev, TTLocalizer.MailboxItemPrev, ''), text_scale=1, text_pos=(
                        0, 0.29999999999999999), text_fg=(
                            1, 1, 1, 1), text_shadow=(
                                0, 0, 0, 1), textMayChange=0, command=self._MailboxScreen__prevItem, state=DGG.DISABLED)
        self.currentItem = None
        self.partyInviteVisual = InviteVisual(self.frame)
        self.partyInviteVisual.setScale(0.72999999999999998)
        self.partyInviteVisual.setPos(0.0, 0.0, 0.47999999999999998)
        self.partyInviteVisual.stash()
        if self.avatar:
            self.avatar.applyCheesyEffect(ToontownGlobals.CENormal)

    def unload(self):
        if self.avatar:
            self.avatar.reconsiderCheesyEffect()

        self._MailboxScreen__clearCurrentItem()
        if hasattr(self, 'frame'):
            self.frame.destroy()
            del self.frame
            self.frameDelStackTrace = StackTrace()
        else:
            self.notify.warning('unload, no self.frame')
        if hasattr(self, 'mailbox'):
            del self.mailbox
        else:
            self.notify.warning('unload, no self.mailbox')
        if self.dialogBox:
            self.dialogBox.cleanup()
            self.dialogBox = None

        for item in self.items:
            if isinstance(item, CatalogItem.CatalogItem):
                item.acceptItemCleanup()
                continue

        self.ignoreAll()

    def justExit(self):
        self._MailboxScreen__acceptExit()

    def _MailboxScreen__handleExit(self):
        if self.numAtticAccepted == 0:
            self._MailboxScreen__acceptExit()
        elif self.numAtticAccepted == 1:
            self.dialogBox = TTDialog.TTDialog(
                style=TTDialog.Acknowledge,
                text=TTLocalizer.CatalogAcceptInAttic,
                text_wordwrap=15,
                command=self._MailboxScreen__acceptExit)
            self.dialogBox.show()
        else:
            self.dialogBox = TTDialog.TTDialog(
                style=TTDialog.Acknowledge,
                text=TTLocalizer.CatalogAcceptInAtticP,
                text_wordwrap=15,
                command=self._MailboxScreen__acceptExit)
            self.dialogBox.show()

    def _MailboxScreen__acceptExit(self, buttonValue=None):
        if hasattr(self, 'frame'):
            self.hide()
            self.unload()
            messenger.send(self.doneEvent)

    def _MailboxScreen__handleAccept(self):
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info('QA-REGRESSION: MAILBOX: Accept item')

        if self.acceptingIndex is not None:
            return None

        item = self.items[self.itemIndex]
        isAward = False
        if isinstance(item, CatalogItem.CatalogItem):
            isAward = item.isAward()

        if not base.cr.isPaid():
            if not isinstance(item, InviteInfoBase):
                pass
            if not isAward:
                TeaserPanel(pageName='clothing')
            else:
                self.acceptingIndex = self.itemIndex
                self.acceptButton['state'] = DGG.DISABLED
                self._MailboxScreen__showCurrentItem()
                item = self.items[self.itemIndex]
                item.acceptItem(
                    self.mailbox,
                    self.acceptingIndex,
                    self._MailboxScreen__acceptItemCallback)

    def _MailboxScreen__handleDiscard(self, buttonValue=None):
        if self.acceptingIndex is not None:
            return None
        elif buttonValue == -1:
            if self.dialogBox:
                self.dialogBox.cleanup()

            self.dialogBox = None
            self._MailboxScreen__showCurrentItem()
        else:
            self.acceptingIndex = self.itemIndex
            self.acceptButton['state'] = DGG.DISABLED
            self._MailboxScreen__showCurrentItem()
            item = self.items[self.itemIndex]
            item.discardItem(
                self.mailbox,
                self.acceptingIndex,
                self._MailboxScreen__discardItemCallback)

    def _MailboxScreen__discardItemCallback(self, retcode, item, index):
        if not hasattr(self, 'frame'):
            return None

        if self.dialogBox:
            self.dialogBox.cleanup()

        self.dialogBox = None
        self.acceptingIndex = None
        self._MailboxScreen__updateItems()
        if isinstance(item, InviteInfoBase):
            callback = self._MailboxScreen__incIndexRemoveDialog
            self.dialogBox = TTDialog.TTDialog(
                style=TTDialog.Acknowledge,
                text=item.getDiscardItemErrorText(retcode),
                text_wordwrap=15,
                command=callback)
            self.dialogBox.show()

    def _MailboxScreen__makeDiscardInterface(self):
        if self.itemIndex >= 0 and self.itemIndex < len(self.items):
            item = self.items[self.itemIndex]
            if isinstance(item, InviteInfoBase):
                itemText = TTLocalizer.MailBoxRejectVerify % self.getItemName(
                    item)
                yesText = TTLocalizer.MailboxReject
            else:
                itemText = TTLocalizer.MailBoxDiscardVerify % self.getItemName(
                    item)
                yesText = TTLocalizer.MailboxDiscard
            self.dialogBox = TTDialog.TTDialog(
                style=TTDialog.TwoChoiceCustom,
                text=itemText,
                text_wordwrap=15,
                command=self._MailboxScreen__handleDiscard,
                buttonText=[
                    yesText,
                    TTLocalizer.MailboxLeave])
            self.dialogBox.show()

    def _MailboxScreen__acceptItemCallback(self, retcode, item, index):
        needtoUpdate = 0
        if self.acceptingIndex is None:
            needtoUpdate = 1

        if not hasattr(self, 'frame'):
            return None

        if retcode == ToontownGlobals.P_UserCancelled:
            print 'mailbox screen user canceled'
            self.acceptingIndex = None
            self._MailboxScreen__updateItems()
            return None

        if self.acceptingIndex != index:
            self.notify.warning(
                'Got unexpected callback for index %s, expected %s.' %
                (index, self.acceptingIndex))
            return None

        self.acceptingIndex = None
        if retcode < 0:
            self.notify.info(
                'Could not take item %s: retcode %s' %
                (item, retcode))
            if retcode == ToontownGlobals.P_NoTrunk:
                self.dialogBox = TTDialog.TTDialog(
                    style=TTDialog.Acknowledge,
                    text=TTLocalizer.CatalogAcceptNoTrunk,
                    text_wordwrap=15,
                    command=self._MailboxScreen__acceptError)
            else:
                self.dialogBox = TTDialog.TTDialog(
                    style=TTDialog.TwoChoiceCustom,
                    text=item.getAcceptItemErrorText(retcode),
                    text_wordwrap=15,
                    command=self._MailboxScreen__handleDiscard,
                    buttonText=[
                        TTLocalizer.MailboxDiscard,
                        TTLocalizer.MailboxLeave])
            self.dialogBox.show()
        elif hasattr(item, 'storedInAttic') and item.storedInAttic():
            self.numAtticAccepted += 1
            self.itemIndex += 1
            if needtoUpdate == 1:
                self._MailboxScreen__updateItems()

        elif isinstance(item, InviteInfoBase):
            self._MailboxScreen__updateItems()

        callback = self._MailboxScreen__incIndexRemoveDialog
        self.dialogBox = TTDialog.TTDialog(
            style=TTDialog.Acknowledge,
            text=item.getAcceptItemErrorText(retcode),
            text_wordwrap=15,
            command=callback)
        self.dialogBox.show()

    def _MailboxScreen__acceptError(self, buttonValue=None):
        self.dialogBox.cleanup()
        self.dialogBox = None
        self._MailboxScreen__showCurrentItem()

    def _MailboxScreen__incIndexRemoveDialog(self, junk=0):
        self._MailboxScreen__incIndex()
        self.dialogBox.cleanup()
        self.dialogBox = None
        self._MailboxScreen__showCurrentItem()

    def _MailboxScreen__incIndex(self, junk=0):
        self.itemIndex += 1

    def _MailboxScreen__acceptOk(self, index, buttonValue=None):
        self.acceptingIndex = None
        if self.dialogBox:
            self.dialogBox.cleanup()
            self.dialogBox = None

        self.items = self.getItems()
        if self.itemIndex > index or self.itemIndex >= len(self.items):
            print 'adjusting item index -1'
            self.itemIndex -= 1

        if len(self.items) < 1:
            self._MailboxScreen__handleExit()
            return None

        self.itemCountLabel['text'] = (
            self._MailboxScreen__getNumberOfItemsText(),)
        self._MailboxScreen__showCurrentItem()

    def _MailboxScreen__refreshItems(self):
        self.acceptingIndex = None
        self._MailboxScreen__updateItems()

    def _MailboxScreen__updateItems(self):
        if self.dialogBox:
            self.dialogBox.cleanup()
            self.dialogBox = None

        self.items = self.getItems()
        if self.itemIndex >= len(self.items):
            print 'adjusting item index -1'
            self.itemIndex = len(self.items) - 1

        if len(self.items) == 0:
            print 'exiting due to lack of items'
            self._MailboxScreen__handleExit()
            return None

        self.itemCountLabel['text'] = (
            self._MailboxScreen__getNumberOfItemsText(),)
        self._MailboxScreen__showCurrentItem()

    def _MailboxScreen__getNumberOfItemsText(self):
        if len(self.items) == 1:
            return TTLocalizer.MailboxOneItem
        else:
            return TTLocalizer.MailboxNumberOfItems % len(self.items)

    def _MailboxScreen__clearCurrentItem(self):
        if self.itemPanel:
            self.itemPanel.destroy()
            self.itemPanel = None

        if self.ival:
            self.ival.finish()
            self.ival = None

        if not self.gettingText.isEmpty():
            self.gettingText.hide()

        if not self.itemText.isEmpty():
            self.itemText.hide()

        if not self.giftTagPanel.isEmpty():
            self.giftTagPanel.hide()

        if not self.acceptButton.isEmpty():
            self.acceptButton['state'] = DGG.DISABLED

        if self.currentItem:
            if isinstance(self.currentItem, CatalogItem.CatalogItem):
                self.currentItem.cleanupPicture()

            self.currentItem = None

    def checkFamily(self, doId):
        for familyMember in base.cr.avList:
            if familyMember.id == doId:
                return familyMember
                continue

    def _MailboxScreen__showCurrentItem(self):
        self._MailboxScreen__clearCurrentItem()
        if len(self.items) < 1:
            self._MailboxScreen__handleExit()
            return None

        self.partyInviteVisual.stash()
        if self.itemIndex + 1 > len(self.items):
            self.itemIndex = len(self.items) - 1

        item = self.items[self.itemIndex]
        if self.itemIndex == self.acceptingIndex:
            self.gettingText['text'] = TTLocalizer.MailboxGettingItem % self.getItemName(
                item)
            self.gettingText.show()
            return None

        self.itemText['text'] = self.getItemName(item)
        self.currentItem = item
        if isinstance(item, CatalogItem.CatalogItem):
            self.acceptButton['text'] = (
                '',
                TTLocalizer.MailboxAcceptButton,
                TTLocalizer.MailboxAcceptButton,
                '')
            self.DiscardButton['text'] = (
                '', TTLocalizer.MailBoxDiscard, TTLocalizer.MailBoxDiscard, '')
            if item.isAward():
                self.giftTagPanel['text'] = TTLocalizer.SpecialEventMailboxStrings[item.specialEventId]
            elif item.giftTag is not None:
                nameOfSender = self.getSenderName(item.giftTag)
                if item.giftCode == ToontownGlobals.GIFT_RAT:
                    self.giftTagPanel['text'] = TTLocalizer.CatalogAcceptRATBeans
                elif item.giftCode == ToontownGlobals.GIFT_partyrefund:
                    self.giftTagPanel['text'] = TTLocalizer.CatalogAcceptPartyRefund
                else:
                    self.giftTagPanel['text'] = TTLocalizer.MailboxGiftTag % nameOfSender
            else:
                self.giftTagPanel['text'] = ''
            (self.itemPanel, self.ival) = item.getPicture(base.localAvatar)
        elif isinstance(item, SimpleMailBase):
            self.acceptButton['text'] = (
                '',
                TTLocalizer.MailboxAcceptButton,
                TTLocalizer.MailboxAcceptButton,
                '')
            self.DiscardButton['text'] = (
                '', TTLocalizer.MailBoxDiscard, TTLocalizer.MailBoxDiscard, '')
            senderId = item.senderId
            nameOfSender = self.getSenderName(senderId)
            self.giftTagPanel['text'] = TTLocalizer.MailFromTag % nameOfSender
            self.itemText['text'] = item.body
        elif isinstance(item, InviteInfoBase):
            self.acceptButton['text'] = (
                '',
                TTLocalizer.MailboxAcceptInvite,
                TTLocalizer.MailboxAcceptInvite,
                '')
            self.DiscardButton['text'] = (
                '',
                TTLocalizer.MailBoxRejectInvite,
                TTLocalizer.MailBoxRejectInvite,
                '')
            partyInfo = None
            for party in self.avatar.partiesInvitedTo:
                if party.partyId == item.partyId:
                    partyInfo = party
                    break
                    continue

            if self.mailbox:
                if item.status == PartyGlobals.InviteStatus.NotRead:
                    self.mailbox.sendInviteReadButNotReplied(item.inviteKey)

            senderId = partyInfo.hostId
            nameOfSender = self.getSenderName(senderId)
            self.giftTagPanel['text'] = ''
            self.itemText['text'] = ''
            self.partyInviteVisual.updateInvitation(nameOfSender, partyInfo)
            self.partyInviteVisual.unstash()
            self.itemPanel = None
            self.ival = None
        else:
            self.acceptButton['text'] = (
                '',
                TTLocalizer.MailboxAcceptButton,
                TTLocalizer.MailboxAcceptButton,
                '')
            self.DiscardButton['text'] = (
                '', TTLocalizer.MailBoxDiscard, TTLocalizer.MailBoxDiscard, '')
            self.giftTagPanel['text'] = ' '
            self.itemPanel = None
            self.ival = None
        self.itemText.show()
        self.giftTagPanel.show()
        if self.itemPanel and item.getTypeName() != TTLocalizer.ChatTypeName:
            self.itemPanel.reparentTo(self.itemBoard, -1)
            self.itemPanel.setPos(0, 0, 0.40000000000000002)
            self.itemPanel.setScale(0.20999999999999999)
            self.itemText['text_wordwrap'] = 16
            self.itemText.setPos(0.0, 0.0, 0.074999999999999997)
        elif isinstance(item, CatalogItem.CatalogItem) and item.getTypeName() == TTLocalizer.ChatTypeName:
            self.itemPanel.reparentTo(self.itemBoard, -1)
            self.itemPanel.setPos(0, 0, 0.34999999999999998)
            self.itemPanel.setScale(0.20999999999999999)
            self.itemText['text_wordwrap'] = 10
            self.itemText.setPos(0, 0, 0.29999999999999999)
        else:
            self.itemText.setPos(0, 0, 0.29999999999999999)
        if self.ival:
            self.ival.loop()

        if self.acceptingIndex is None:
            self.acceptButton['state'] = DGG.NORMAL

        if self.itemIndex > 0:
            self.prevButton['state'] = DGG.NORMAL
        else:
            self.prevButton['state'] = DGG.DISABLED
        if self.itemIndex + 1 < len(self.items):
            self.nextButton['state'] = DGG.NORMAL
        else:
            self.nextButton['state'] = DGG.DISABLED

    def _MailboxScreen__nextItem(self):
        messenger.send('wakeup')
        if self.itemIndex + 1 < len(self.items):
            self.itemIndex += 1
            self._MailboxScreen__showCurrentItem()

    def _MailboxScreen__prevItem(self):
        messenger.send('wakeup')
        if self.itemIndex > 0:
            self.itemIndex -= 1
            self._MailboxScreen__showCurrentItem()

    def getItemName(self, item):
        if isinstance(item, CatalogItem.CatalogItem):
            return item.getName()
        elif isinstance(item, str):
            return TTLocalizer.MailSimpleMail
        elif isinstance(item, InviteInfoBase):
            return TTLocalizer.InviteInvitation
        else:
            return ''

    def getItems(self):
        result = []
        result = self.avatar.awardMailboxContents[:]
        result += self.avatar.mailboxContents[:]
        if self.avatar.mail:
            result += self.avatar.mail

        mailboxInvites = self.avatar.getInvitesToShowInMailbox()
        if mailboxInvites:
            result += mailboxInvites

        return result

    def getNumberOfAwardItems(self):
        result = 0
        for item in self.items:
            if isinstance(
                    item,
                    CatalogItem.CatalogItem) and item.specialEventId > 0:
                result += 1
                continue
            break

        return result

    def getSenderName(self, avId):
        sender = base.cr.identifyFriend(avId)
        nameOfSender = ''
        if sender:
            nameOfSender = sender.getName()
        else:
            sender = self.checkFamily(avId)
            if sender:
                nameOfSender = sender.name
            elif hasattr(base.cr, 'playerFriendsManager'):
                sender = base.cr.playerFriendsManager.getAvHandleFromId(avId)
                if sender:
                    nameOfSender = sender.getName()

        if not sender:
            nameOfSender = TTLocalizer.MailboxGiftTagAnonymous
            if hasattr(base.cr, 'playerFriendsManager'):
                base.cr.playerFriendsManager.requestAvatarInfo(avId)
                self.accept(
                    'friendsListChanged',
                    self._MailboxScreen__showCurrentItem)

        return nameOfSender
