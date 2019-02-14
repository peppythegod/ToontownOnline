from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
import CatalogItemTypes
import CatalogItem
from CatalogWallpaperItem import getAllWallpapers
from CatalogFlooringItem import getAllFloorings
from CatalogMouldingItem import getAllMouldings
from CatalogWainscotingItem import getAllWainscotings
from CatalogFurnitureItem import getAllFurnitures
from CatalogFurnitureItem import FLTrunk
from toontown.toontowngui.TeaserPanel import TeaserPanel
from otp.otpbase import OTPGlobals
from direct.directnotify import DirectNotifyGlobal
CATALOG_PANEL_WORDWRAP = 10
CATALOG_PANEL_CHAT_WORDWRAP = 9
CATALOG_PANEL_ACCESSORY_WORDWRAP = 11


class CatalogItemPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CatalogItemPanel')

    def __init__(self, parent=aspect2d, parentCatalogScreen=None, **kw):
        optiondefs = (('item', None, DGG.INITOPT),
                      ('type', CatalogItem.CatalogTypeUnspecified,
                       DGG.INITOPT), ('relief', None, None))
        self.parentCatalogScreen = parentCatalogScreen
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.loaded = 0
        self.initialiseoptions(CatalogItemPanel)

    def load(self):
        if self.loaded:
            return None

        self.loaded = 1
        self.verify = None
        self.pictureFrame = self.attachNewNode('pictureFrame')
        self.pictureFrame.setScale(0.14999999999999999)
        self.itemIndex = 0
        self.ival = None
        typeCode = self['item'].getTypeCode()
        if self['item'].needsCustomize():
            if typeCode == CatalogItemTypes.WALLPAPER_ITEM and typeCode == CatalogItemTypes.FLOORING_ITEM and typeCode == CatalogItemTypes.MOULDING_ITEM and typeCode == CatalogItemTypes.FURNITURE_ITEM and typeCode == CatalogItemTypes.WAINSCOTING_ITEM or typeCode == CatalogItemTypes.TOON_STATUE_ITEM:
                if typeCode == CatalogItemTypes.WALLPAPER_ITEM:
                    self.items = getAllWallpapers(self['item'].patternIndex)
                elif typeCode == CatalogItemTypes.FLOORING_ITEM:
                    self.items = getAllFloorings(self['item'].patternIndex)
                elif typeCode == CatalogItemTypes.MOULDING_ITEM:
                    self.items = getAllMouldings(self['item'].patternIndex)
                elif typeCode == CatalogItemTypes.FURNITURE_ITEM:
                    self.items = getAllFurnitures(self['item'].furnitureType)
                elif typeCode == CatalogItemTypes.TOON_STATUE_ITEM:
                    self.items = self['item'].getAllToonStatues()
                elif typeCode == CatalogItemTypes.WAINSCOTING_ITEM:
                    self.items = getAllWainscotings(self['item'].patternIndex)

                self.numItems = len(self.items)
                if self.numItems > 1:
                    guiItems = loader.loadModel(
                        'phase_5.5/models/gui/catalog_gui')
                    nextUp = guiItems.find('**/arrow_up')
                    nextRollover = guiItems.find('**/arrow_Rollover')
                    nextDown = guiItems.find('**/arrow_Down')
                    prevUp = guiItems.find('**/arrowUp')
                    prevDown = guiItems.find('**/arrowDown1')
                    prevRollover = guiItems.find('**/arrowRollover')
                    self.nextVariant = DirectButton(
                        parent=self,
                        relief=None,
                        image=(nextUp, nextDown, nextRollover, nextUp),
                        image3_color=(1, 1, 1, 0.40000000000000002),
                        pos=(0.13, 0, 0),
                        command=self.showNextVariant)
                    self.prevVariant = DirectButton(
                        parent=self,
                        relief=None,
                        image=(prevUp, prevDown, prevRollover, prevUp),
                        image3_color=(1, 1, 1, 0.40000000000000002),
                        pos=(-0.13, 0, 0),
                        command=self.showPrevVariant,
                        state=DGG.DISABLED)
                    self.variantPictures = [(None, None)] * self.numItems
                else:
                    self.variantPictures = [(None, None)]
                self.showCurrentVariant()
            else:
                (picture,
                 self.ival) = self['item'].getPicture(base.localAvatar)
                if picture:
                    picture.reparentTo(self)
                    picture.setScale(0.14999999999999999)

                self.items = [self['item']]
                self.variantPictures = [(picture, self.ival)]
        self.typeLabel = DirectLabel(
            parent=self,
            relief=None,
            pos=(0, 0, 0.23999999999999999),
            scale=TTLocalizer.CIPtypeLabel,
            text=self['item'].getTypeName(),
            text_fg=(0.94999999999999996, 0.94999999999999996, 0, 1),
            text_shadow=(0, 0, 0, 1),
            text_font=ToontownGlobals.getInterfaceFont(),
            text_wordwrap=CATALOG_PANEL_WORDWRAP)
        self.auxText = DirectLabel(
            parent=self,
            relief=None,
            scale=0.050000000000000003,
            pos=(-0.20000000000000001, 0, 0.16))
        self.auxText.setHpr(0, 0, -30)
        self.nameLabel = DirectLabel(
            parent=self,
            relief=None,
            text=self['item'].getDisplayName(),
            text_fg=(0, 0, 0, 1),
            text_font=ToontownGlobals.getInterfaceFont(),
            text_scale=TTLocalizer.CIPnameLabel,
            text_wordwrap=CATALOG_PANEL_WORDWRAP +
            TTLocalizer.CIPwordwrapOffset)
        if self['item'].getTypeCode() == CatalogItemTypes.CHAT_ITEM:
            self.nameLabel['text_wordwrap'] = CATALOG_PANEL_CHAT_WORDWRAP
            numRows = self.nameLabel.component('text0').textNode.getNumRows()
            if numRows == 1:
                namePos = (0, 0, -0.059999999999999998)
            elif numRows == 2:
                namePos = (0, 0, -0.029999999999999999)
            else:
                namePos = (0, 0, 0)
            nameScale = 0.063
        elif self['item'].getTypeCode() == CatalogItemTypes.ACCESSORY_ITEM:
            self.nameLabel['text_wordwrap'] = CATALOG_PANEL_ACCESSORY_WORDWRAP
            namePos = (0, 0, -0.22)
            nameScale = 0.059999999999999998
        else:
            namePos = (0, 0, -0.22)
            nameScale = 0.059999999999999998
        self.nameLabel.setPos(*namePos)
        self.nameLabel.setScale(nameScale)
        numericBeanPrice = self['item'].getPrice(self['type'])
        priceStr = str(numericBeanPrice) + ' ' + TTLocalizer.CatalogCurrency
        priceScale = 0.070000000000000007
        if self['item'].isSaleItem():
            priceStr = TTLocalizer.CatalogSaleItem + priceStr
            priceScale = 0.059999999999999998

        self.priceLabel = DirectLabel(
            parent=self,
            relief=None,
            pos=(0, 0, -0.29999999999999999),
            scale=priceScale,
            text=priceStr,
            text_fg=(0.94999999999999996, 0.94999999999999996, 0, 1),
            text_shadow=(0, 0, 0, 1),
            text_font=ToontownGlobals.getSignFont(),
            text_align=TextNode.ACenter)
        self.createEmblemPrices(numericBeanPrice)
        buttonModels = loader.loadModel('phase_3.5/models/gui/inventory_gui')
        upButton = buttonModels.find('**/InventoryButtonUp')
        downButton = buttonModels.find('**/InventoryButtonDown')
        rolloverButton = buttonModels.find('**/InventoryButtonRollover')
        buyText = TTLocalizer.CatalogBuyText
        buyTextScale = TTLocalizer.CIPbuyButton
        if self['item'].isRental():
            buyText = TTLocalizer.CatalogRentText

        self.buyButton = DirectButton(
            parent=self,
            relief=None,
            pos=(0.20000000000000001, 0, 0.14999999999999999),
            scale=(0.69999999999999996, 1, 0.80000000000000004),
            text=buyText,
            text_scale=buyTextScale,
            text_pos=(-0.0050000000000000001, -0.01),
            image=(upButton, downButton, rolloverButton, upButton),
            image_color=(1.0, 0.20000000000000001, 0.20000000000000001, 1),
            image0_color=Vec4(1.0, 0.40000000000000002, 0.40000000000000002,
                              1),
            image3_color=Vec4(1.0, 0.40000000000000002, 0.40000000000000002,
                              0.40000000000000002),
            command=self._CatalogItemPanel__handlePurchaseRequest)
        soundIcons = loader.loadModel('phase_5.5/models/gui/catalogSoundIcons')
        soundOn = soundIcons.find('**/sound07')
        soundOff = soundIcons.find('**/sound08')
        self.soundOnButton = DirectButton(
            parent=self,
            relief=None,
            pos=(0.20000000000000001, 0, -0.14999999999999999),
            scale=(0.69999999999999996, 1, 0.80000000000000004),
            text_scale=buyTextScale,
            text_pos=(-0.0050000000000000001, -0.01),
            image=(upButton, downButton, rolloverButton, upButton),
            image_color=(0.20000000000000001, 0.5, 0.20000000000000001, 1),
            image0_color=Vec4(0.40000000000000002, 0.5, 0.40000000000000002,
                              1),
            image3_color=Vec4(0.40000000000000002, 0.5, 0.40000000000000002,
                              0.40000000000000002),
            command=self.handleSoundOnButton)
        self.soundOnButton.hide()
        soundOn.setScale(0.10000000000000001)
        soundOn.reparentTo(self.soundOnButton)
        self.soundOffButton = DirectButton(
            parent=self,
            relief=None,
            pos=(0.20000000000000001, 0, -0.14999999999999999),
            scale=(0.69999999999999996, 1, 0.80000000000000004),
            text_scale=buyTextScale,
            text_pos=(-0.0050000000000000001, -0.01),
            image=(upButton, downButton, rolloverButton, upButton),
            image_color=(0.20000000000000001, 1.0, 0.20000000000000001, 1),
            image0_color=Vec4(0.40000000000000002, 1.0, 0.40000000000000002,
                              1),
            image3_color=Vec4(0.40000000000000002, 1.0, 0.40000000000000002,
                              0.40000000000000002),
            command=self.handleSoundOffButton)
        self.soundOffButton.hide()
        soundOff = self.soundOffButton.attachNewNode('soundOff')
        soundOn.copyTo(soundOff)
        soundOff.reparentTo(self.soundOffButton)
        upGButton = buttonModels.find('**/InventoryButtonUp')
        downGButton = buttonModels.find('**/InventoryButtonDown')
        rolloverGButton = buttonModels.find('**/InventoryButtonRollover')
        self.giftButton = DirectButton(
            parent=self,
            relief=None,
            pos=(0.20000000000000001, 0, 0.14999999999999999),
            scale=(0.69999999999999996, 1, 0.80000000000000004),
            text=TTLocalizer.CatalogGiftText,
            text_scale=buyTextScale,
            text_pos=(-0.0050000000000000001, -0.01),
            image=(upButton, downButton, rolloverButton, upButton),
            image_color=(1.0, 0.20000000000000001, 0.20000000000000001, 1),
            image0_color=Vec4(1.0, 0.40000000000000002, 0.40000000000000002,
                              1),
            image3_color=Vec4(1.0, 0.40000000000000002, 0.40000000000000002,
                              0.40000000000000002),
            command=self._CatalogItemPanel__handleGiftRequest)
        self.updateButtons()

    def createEmblemPrices(self, numericBeanPrice):
        priceScale = 0.070000000000000007
        emblemPrices = self['item'].getEmblemPrices()
        if emblemPrices:
            if numericBeanPrice:
                self.priceLabel.hide()
                beanModel = loader.loadModel(
                    'phase_5.5/models/estate/jellyBean')
                beanModel.setColorScale(1, 0, 0, 1)
                self.beanPriceLabel = DirectLabel(
                    parent=self,
                    relief=None,
                    pos=(0, 0, -0.29999999999999999),
                    scale=priceScale,
                    image=beanModel,
                    image_pos=(-0.40000000000000002, 0, 0.40000000000000002),
                    text=str(numericBeanPrice),
                    text_fg=(0.94999999999999996, 0.94999999999999996, 0, 1),
                    text_shadow=(0, 0, 0, 1),
                    text_font=ToontownGlobals.getSignFont(),
                    text_align=TextNode.ALeft)
            else:
                self.priceLabel.hide()
            goldPrice = 0
            silverPrice = 0
            emblemIcon = loader.loadModel(
                'phase_3.5/models/gui/tt_m_gui_gen_emblemIcons')
            silverModel = emblemIcon.find('**/tt_t_gui_gen_emblemSilver')
            goldModel = emblemIcon.find('**/tt_t_gui_gen_emblemGold')
            if ToontownGlobals.EmblemTypes.Silver < len(emblemPrices):
                silverPrice = emblemPrices[ToontownGlobals.EmblemTypes.Silver]
                if silverPrice:
                    self.silverPriceLabel = DirectLabel(
                        parent=self,
                        relief=None,
                        pos=(0, 0, -0.29999999999999999),
                        scale=priceScale,
                        image=silverModel,
                        image_pos=(-0.40000000000000002, 0,
                                   0.40000000000000002),
                        text=str(silverPrice),
                        text_fg=(0.94999999999999996, 0.94999999999999996, 0,
                                 1),
                        text_shadow=(0, 0, 0, 1),
                        text_font=ToontownGlobals.getSignFont(),
                        text_align=TextNode.ALeft)

            if ToontownGlobals.EmblemTypes.Gold < len(emblemPrices):
                goldPrice = emblemPrices[ToontownGlobals.EmblemTypes.Gold]
                if goldPrice:
                    self.goldPriceLabel = DirectLabel(
                        parent=self,
                        relief=None,
                        pos=(0, 0, -0.29999999999999999),
                        scale=priceScale,
                        image=goldModel,
                        image_pos=(-0.40000000000000002, 0,
                                   0.40000000000000002),
                        text=str(goldPrice),
                        text_fg=(0.94999999999999996, 0.94999999999999996, 0,
                                 1),
                        text_shadow=(0, 0, 0, 1),
                        text_font=ToontownGlobals.getSignFont(),
                        text_align=TextNode.ALeft)

            numPrices = 0
            if numericBeanPrice:
                numPrices += 1

            if silverPrice:
                numPrices += 1

            if goldPrice:
                numPrices += 1

            if numPrices == 2:
                if not numericBeanPrice:
                    self.silverPriceLabel.setX(-0.14999999999999999)
                    self.goldPriceLabel.setX(0.14999999999999999)

                if not silverPrice:
                    self.goldPriceLabel.setX(-0.14999999999999999)
                    self.beanPriceLabel.setX(0.14999999999999999)

                if not goldPrice:
                    self.silverPriceLabel.setX(-0.14999999999999999)
                    self.beanPriceLabel.setX(0.14999999999999999)

            elif numPrices == 3:
                self.silverPriceLabel.setX(-0.20000000000000001)
                self.goldPriceLabel.setX(0)
                self.beanPriceLabel.setX(0.14999999999999999)

    def showNextVariant(self):
        messenger.send('wakeup')
        self.hideCurrentVariant()
        self.itemIndex += 1
        if self.itemIndex >= self.numItems - 1:
            self.itemIndex = self.numItems - 1
            self.nextVariant['state'] = DGG.DISABLED
        else:
            self.nextVariant['state'] = DGG.NORMAL
        self.prevVariant['state'] = DGG.NORMAL
        self.showCurrentVariant()

    def showPrevVariant(self):
        messenger.send('wakeup')
        self.hideCurrentVariant()
        self.itemIndex -= 1
        if self.itemIndex < 0:
            self.itemIndex = 0
            self.prevVariant['state'] = DGG.DISABLED
        else:
            self.prevVariant['state'] = DGG.NORMAL
        self.nextVariant['state'] = DGG.NORMAL
        self.showCurrentVariant()

    def showCurrentVariant(self):
        (newPic, self.ival) = self.variantPictures[self.itemIndex]
        if self.ival:
            self.ival.finish()

        if not newPic:
            variant = self.items[self.itemIndex]
            (newPic, self.ival) = variant.getPicture(base.localAvatar)
            self.variantPictures[self.itemIndex] = (newPic, self.ival)

        newPic.reparentTo(self.pictureFrame)
        if self.ival:
            self.ival.loop()

        if self['item'].getTypeCode() == CatalogItemTypes.TOON_STATUE_ITEM:
            if hasattr(self, 'nameLabel'):
                self.nameLabel['text'] = self.items[
                    self.itemIndex].getDisplayName()
                self['item'].gardenIndex = self.items[
                    self.itemIndex].gardenIndex

    def hideCurrentVariant(self):
        currentPic = self.variantPictures[self.itemIndex][0]
        if currentPic:
            currentPic.detachNode()

    def unload(self):
        if not self.loaded:
            DirectFrame.destroy(self)
            return None

        self.loaded = 0
        if self['item'].getTypeCode() == CatalogItemTypes.TOON_STATUE_ITEM:
            self['item'].deleteAllToonStatues()
            self['item'].gardenIndex = self['item'].startPoseIndex
            self.nameLabel['text'] = self['item'].getDisplayName()

        self['item'].requestPurchaseCleanup()
        for (picture, ival) in self.variantPictures:
            if picture:
                picture.destroy()

            if ival:
                ival.finish()
                continue

        self.variantPictures = None
        if self.ival:
            self.ival.finish()

        self.ival = None
        if len(self.items):
            self.items[0].cleanupPicture()

        self.pictureFrame.remove()
        self.pictureFrame = None
        self.items = []
        if self.verify:
            self.verify.cleanup()

        DirectFrame.destroy(self)

    def destroy(self):
        self.parentCatalogScreen = None
        self.unload()

    def getTeaserPanel(self):
        typeName = self['item'].getTypeName()
        if typeName == TTLocalizer.EmoteTypeName or typeName == TTLocalizer.ChatTypeName:
            page = 'emotions'
        elif typeName == TTLocalizer.GardenTypeName or typeName == TTLocalizer.GardenStarterTypeName:
            page = 'gardening'
        else:
            page = 'clothing'

        def showTeaserPanel():
            TeaserPanel(pageName=page)

        return showTeaserPanel

    def updateBuyButton(self):
        if not self.loaded:
            return None

        if not base.cr.isPaid():
            self.buyButton['command'] = self.getTeaserPanel()

        self.buyButton.show()
        typeCode = self['item'].getTypeCode()
        orderCount = base.localAvatar.onOrder.count(self['item'])
        if orderCount > 0:
            if orderCount > 1:
                auxText = '%d %s' % (orderCount,
                                     TTLocalizer.CatalogOnOrderText)
            else:
                auxText = TTLocalizer.CatalogOnOrderText
        else:
            auxText = ''
        isNameTag = typeCode == CatalogItemTypes.NAMETAG_ITEM
        if isNameTag and not (
                localAvatar.getGameAccess() == OTPGlobals.AccessFull):
            if self['item'].nametagStyle == 100:
                if localAvatar.getFont() == ToontownGlobals.getToonFont():
                    auxText = TTLocalizer.CatalogCurrent
                    self.buyButton['state'] = DGG.DISABLED

            elif self['item'].getPrice(
                    self['type']
            ) > base.localAvatar.getMoney() + base.localAvatar.getBankMoney():
                self.buyButton['state'] = DGG.DISABLED

        elif isNameTag and self[
                'item'].nametagStyle == localAvatar.getNametagStyle():
            auxText = TTLocalizer.CatalogCurrent
            self.buyButton['state'] = DGG.DISABLED
        elif self['item'].reachedPurchaseLimit(base.localAvatar):
            max = self['item'].getPurchaseLimit()
            if max <= 1:
                auxText = TTLocalizer.CatalogPurchasedText
                if self['item'].hasBeenGifted(base.localAvatar):
                    auxText = TTLocalizer.CatalogGiftedText

            else:
                auxText = TTLocalizer.CatalogPurchasedMaxText
            self.buyButton['state'] = DGG.DISABLED
        elif hasattr(self['item'], 'noGarden') and self['item'].noGarden(
                base.localAvatar):
            auxText = TTLocalizer.NoGarden
            self.buyButton['state'] = DGG.DISABLED
        elif hasattr(self['item'],
                     'isSkillTooLow') and self['item'].isSkillTooLow(
                         base.localAvatar):
            auxText = TTLocalizer.SkillTooLow
            self.buyButton['state'] = DGG.DISABLED
        elif hasattr(self['item'], 'getDaysToGo') and self['item'].getDaysToGo(
                base.localAvatar):
            auxText = TTLocalizer.DaysToGo % self['item'].getDaysToGo(
                base.localAvatar)
            self.buyButton['state'] = DGG.DISABLED
        elif self['item'].getEmblemPrices(
        ) and not base.localAvatar.isEnoughMoneyAndEmblemsToBuy(
                self['item'].getPrice(self['type']),
                self['item'].getEmblemPrices()):
            self.buyButton['state'] = DGG.DISABLED
        elif self['item'].getPrice(
                self['type']
        ) <= base.localAvatar.getMoney() + base.localAvatar.getBankMoney():
            self.buyButton['state'] = DGG.NORMAL
            self.buyButton.show()
        else:
            self.buyButton['state'] = DGG.DISABLED
            self.buyButton.show()
        self.auxText['text'] = auxText

    def _CatalogItemPanel__handlePurchaseRequest(self):
        if self['item'].replacesExisting() and self['item'].hasExisting():
            if self['item'].getFlags() & FLTrunk:
                message = TTLocalizer.CatalogVerifyPurchase % {
                    'item': self['item'].getName(),
                    'price': self['item'].getPrice(self['type'])
                }
            else:
                message = TTLocalizer.CatalogOnlyOnePurchase % {
                    'old': self['item'].getYourOldDesc(),
                    'item': self['item'].getName(),
                    'price': self['item'].getPrice(self['type'])
                }
        elif self['item'].isRental():
            message = TTLocalizer.CatalogVerifyRent % {
                'item': self['item'].getName(),
                'price': self['item'].getPrice(self['type'])
            }
        else:
            emblemPrices = self['item'].getEmblemPrices()
            if emblemPrices:
                silver = emblemPrices[ToontownGlobals.EmblemTypes.Silver]
                gold = emblemPrices[ToontownGlobals.EmblemTypes.Gold]
                price = self['item'].getPrice(self['type'])
                if price and silver and gold:
                    message = TTLocalizer.CatalogVerifyPurchaseBeanSilverGold % {
                        'item': self['item'].getName(),
                        'price': self['item'].getPrice(self['type']),
                        'silver': silver,
                        'gold': gold
                    }
                elif price and silver:
                    message = TTLocalizer.CatalogVerifyPurchaseBeanSilver % {
                        'item': self['item'].getName(),
                        'price': self['item'].getPrice(self['type']),
                        'silver': silver,
                        'gold': gold
                    }
                elif price and gold:
                    message = TTLocalizer.CatalogVerifyPurchaseBeanGold % {
                        'item': self['item'].getName(),
                        'price': self['item'].getPrice(self['type']),
                        'silver': silver,
                        'gold': gold
                    }
                elif silver and gold:
                    message = TTLocalizer.CatalogVerifyPurchaseSilverGold % {
                        'item': self['item'].getName(),
                        'price': self['item'].getPrice(self['type']),
                        'silver': silver,
                        'gold': gold
                    }
                elif silver:
                    message = TTLocalizer.CatalogVerifyPurchaseSilver % {
                        'item': self['item'].getName(),
                        'price': self['item'].getPrice(self['type']),
                        'silver': silver,
                        'gold': gold
                    }
                elif gold:
                    message = TTLocalizer.CatalogVerifyPurchaseGold % {
                        'item': self['item'].getName(),
                        'price': self['item'].getPrice(self['type']),
                        'silver': silver,
                        'gold': gold
                    }
                else:
                    self.notify.warning('is this a completely free item %s?' %
                                        self['item'].getName())
                    message = TTLocalizer.CatalogVerifyPurchase % {
                        'item': self['item'].getName(),
                        'price': self['item'].getPrice(self['type'])
                    }
            else:
                message = TTLocalizer.CatalogVerifyPurchase % {
                    'item': self['item'].getName(),
                    'price': self['item'].getPrice(self['type'])
                }
        self.verify = TTDialog.TTGlobalDialog(
            doneEvent='verifyDone', message=message, style=TTDialog.TwoChoice)
        self.verify.show()
        self.accept('verifyDone', self._CatalogItemPanel__handleVerifyPurchase)

    def _CatalogItemPanel__handleVerifyPurchase(self):
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info('QA-REGRESSION: CATALOG: Order item')

        status = self.verify.doneStatus
        self.ignore('verifyDone')
        self.verify.cleanup()
        del self.verify
        self.verify = None
        if status == 'ok':
            item = self.items[self.itemIndex]
            messenger.send('CatalogItemPurchaseRequest', [item])
            self.buyButton['state'] = DGG.DISABLED

    def _CatalogItemPanel__handleGiftRequest(self):
        if self['item'].replacesExisting() and self['item'].hasExisting():
            message = TTLocalizer.CatalogOnlyOnePurchase % {
                'old': self['item'].getYourOldDesc(),
                'item': self['item'].getName(),
                'price': self['item'].getPrice(self['type'])
            }
        else:
            friendIndex = self.parentCatalogScreen.friendGiftIndex
            friendText = 'Error'
            numFriends = len(base.localAvatar.friendsList) + \
                len(base.cr.avList) - 1
            if numFriends > 0:
                friendText = self.parentCatalogScreen.receiverName

            message = TTLocalizer.CatalogVerifyGift % {
                'item': self['item'].getName(),
                'price': self['item'].getPrice(self['type']),
                'friend': friendText
            }
        self.verify = TTDialog.TTGlobalDialog(
            doneEvent='verifyGiftDone',
            message=message,
            style=TTDialog.TwoChoice)
        self.verify.show()
        self.accept('verifyGiftDone', self._CatalogItemPanel__handleVerifyGift)

    def _CatalogItemPanel__handleVerifyGift(self):
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info('QA-REGRESSION: CATALOG: Gift item')

        status = self.verify.doneStatus
        self.ignore('verifyGiftDone')
        self.verify.cleanup()
        del self.verify
        self.verify = None
        if status == 'ok':
            self.giftButton['state'] = DGG.DISABLED
            item = self.items[self.itemIndex]
            messenger.send('CatalogItemGiftPurchaseRequest', [item])

    def updateButtons(self, giftActivate=0):
        if self.parentCatalogScreen.gifting == -1:
            self.updateBuyButton()
            if self.loaded:
                self.giftButton.hide()

        else:
            self.updateGiftButton(giftActivate)
            if self.loaded:
                self.buyButton.hide()

    def updateGiftButton(self, giftUpdate=0):
        if not self.loaded:
            return None

        self.giftButton.show()
        if giftUpdate == 0:
            return None

        if not base.cr.isPaid():
            self.giftButton['command'] = self.getTeaserPanel()

        self.auxText['text'] = ' '
        numFriends = len(base.localAvatar.friendsList) + \
            len(base.cr.avList) - 1
        if numFriends > 0:
            self.giftButton['state'] = DGG.DISABLED
            self.giftButton.show()
            auxText = ' '
            if self['item'].isGift() <= 0:
                self.giftButton.show()
                self.giftButton['state'] = DGG.DISABLED
                auxText = TTLocalizer.CatalogNotAGift
                self.auxText['text'] = auxText
                return None
            elif self.parentCatalogScreen.gotAvatar == 1:
                avatar = self.parentCatalogScreen.giftAvatar
                if (self['item'].forBoysOnly()
                        or avatar.getStyle().getGender() == 'f'
                        or self['item'].forGirlsOnly()
                    ) and avatar.getStyle().getGender() == 'm':
                    self.giftButton.show()
                    self.giftButton['state'] = DGG.DISABLED
                    auxText = TTLocalizer.CatalogNoFit
                    self.auxText['text'] = auxText
                    return None
                elif self['item'].reachedPurchaseLimit(avatar):
                    self.giftButton.show()
                    self.giftButton['state'] = DGG.DISABLED
                    auxText = TTLocalizer.CatalogPurchasedGiftText
                    self.auxText['text'] = auxText
                    return None
                elif len(avatar.mailboxContents) + len(
                        avatar.onGiftOrder
                ) >= ToontownGlobals.MaxMailboxContents:
                    self.giftButton.show()
                    self.giftButton['state'] = DGG.DISABLED
                    auxText = TTLocalizer.CatalogMailboxFull
                    self.auxText['text'] = auxText
                    return None
                elif self['item'].getPrice(
                        self['type']) <= base.localAvatar.getMoney(
                        ) + base.localAvatar.getBankMoney():
                    self.giftButton['state'] = DGG.NORMAL
                    self.giftButton.show()

    def handleSoundOnButton(self):
        item = self.items[self.itemIndex]
        self.soundOnButton.hide()
        self.soundOffButton.show()
        if hasattr(item, 'changeIval'):
            if self.ival:
                self.ival.finish()
                self.ival = None

            self.ival = item.changeIval(volume=1)
            self.ival.loop()

    def handleSoundOffButton(self):
        item = self.items[self.itemIndex]
        self.soundOffButton.hide()
        self.soundOnButton.show()
        if hasattr(item, 'changeIval'):
            if self.ival:
                self.ival.finish()
                self.ival = None

            self.ival = item.changeIval(volume=0)
            self.ival.loop()
