import wx

# width of main frame
WIDTH = 1280
# height of main frame
HEIGHT = 720

# size (width + height) of the (dummy?) elements
ELEMENT_SIZE = 100
# their border
BORDER = 10
# just for shorter and summarized code
FULL_ELEMENT = ELEMENT_SIZE + 2 * BORDER

# message types
# style-flags:
# wx.OK	                Show an OK button.
# wx.CANCEL	            Show a Cancel button.
# wx.YES_NO	            Show Yes and No buttons.
# wx.YES_DEFAULT	      Used with wxYES_NO, makes Yes button the default -
#                         which is the default behaviour.
# wx.NO_DEFAULT	        Used with wxYES_NO, makes No button the default.
# wx.ICON_EXCLAMATION	  Shows an exclamation mark icon.
# wx.ICON_HAND	        Shows an error icon.
# wx.ICON_ERROR	        Shows an error icon - the same as wxICON_HAND.
# wx.ICON_QUESTION	    Shows a question mark icon.
# wx.ICON_INFORMATION	  Shows an information (i) icon.
# wx.STAY_ON_TOP	      The message box stays on top of all other window, even
#                         those of the other applications (Windows only).
MSG_ERR = wx.ICON_ERROR | wx.STAY_ON_TOP | wx.CANCEL
MSG_WRN = wx.ICON_EXCLAMATION | wx.OK | wx.CANCEL
MSG_INF = wx.ICON_INFORMATION | wx.OK
