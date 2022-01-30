#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Draw interactive arrows in GIMP, using a path as a guide for where to draw.

 ===================================================================================================
 Inspired by 'arrowdesigner-0.5' of Akkana Peck, at «http://www.shallowsky.com/software»\
    and 'arrow.scm' of Berengar W. Lehr, thanks.

 Plug-in history:
 Version 0.1 (2012/01/24): 'ArrowsCreator' by Robert Brizard. Tested on GIMP-2.6
 Version 0.2.0 (2013/04/11): adapted to GIMP-2.8 (can no longer vary brush size with\
        GIMP while...),
     +introduce a configuration file,
     +more differences between arrow type 0 and type 1,
     +a notched arrow type and
     +revised instructions at the window top.
 Version 0.2.2 (2014/03/21): armouring against missing element due to user,
     +avoid duplicate plug-in launch and
     +add to the configuration file.
 Version 0.3.0 (2015/02/16): for the brush way in GIMP-2.8.14
     +new shape head control for style: "Arrow with disk joint",
     +use one layer-group for the plug-in with the layer parasite of 'info_layers.py',
     +include computer 'sluggishness' in the configuration file,
     +separate first anchors placement from the arrow 'update()' and employ path tattoo,
     +added a line 'Relative to previous...' in 'Status' frame.
 Version 0.3.2 (2015/06/05):
     +make layer type conform with image base_type (bug: only RGB before!),
     +use pattern head fill, if top of pattern list (index 0) then foreground colour\
        fill as before (default).
     +avoid an error if the user deletes the two anchors
     +in general: trying to improve text messages and streamlining the code
 Version 0.3.3 (2015/10/26):
     +add to 'Relative to previous...', the start coords of previous (trying to \
        distinguish many elements on same layer). So now the link from previous won't\
        work with image from AC version < 0.3.3 ,
     +display some info, at start, about the date in group layer,
     +keep last AC path ("AC_vectors") at closing to resume later (pro: save two pointing \
        and l-clicking; con: don't start the same way).
 Version 0.3.4 (2016/08/17): looking at some details
     +improve: the configuration info and its management by doing automatic 'touch' now,\
        on the plug-in during configuration. (unable to use 'Ctrl+x' on Windows for text entry?)
     +include the index of the restricted pattern, used for the default FG head-fill,\
        in the configuration file so able to choose a more 'unusable' pattern (default = 4\
        index of 'Blue Grid' on my system).
     +handling of some of the user error at the beginning of function 'update()' for\
        the arrow is probably neater, for a missing image or AC_group-layer or 'AC_vectors'.
     +in general: re-factoring for AC-0.3 because of previous changes.
 Version 0.3.5 (2016/09/18): looking at 'labelling arrow'
     +may put a label inside the tail circle if the button 'Next element' is click after\
        a suitable 'Labelling arrow',
     +resuming for the labels too,
     +implement Rod Detmer text-layer saving if it has: label + separator + text.\
        Treating the windows differently for each OS during the label writing, make the\
        ab AC_argmenu is the link from 'MenuArrowsCreator_4' to ArrowsCreatorove more dependable,\
        here for Linux,
     +remove a couple of bugs, for example: if no 'label-info' parasite; the other being\
        start 'self.pre_char = 0' in __init__(),
     +better for resuming is saving also the proposed label at closing time.
     +Tweak the size of the text-layer for complete label soft outline display (more\
        successful than before).
     +(2016/11/20) a bit more armouring and tweaking and label max length is now 3 bytes.
     +(2016/12/10) the coloured text has now a background (to be readable irrespective of\
        the theme) and it permits a group administration installation in Linux by decoupling the\
        configuration and translation folder from the plug-in place.
     +(2017/02/25) patch the missing case of the head length greater than the whole arrow length,
        for style 6.
 Version 0.4.0 (2017/03/01): from GIMP-2.8.14 to 2.10.
    In the plug-in UI a new button: 'Redraw the above arrow', for performance reason, so no longer \
        the automatic arrow during a GIMP anchor-path drag.
    Status part of UI has an asterisk now after the 'Element' number to indicate label possibility.
    Make a curvy edge head for the path arrow, its more style 6 but had to use 'Redraw ...' and\
        it use now both foreground colour in the shaft, background in tail and (if default \
        pattern) head; for that arrow style.
    Associate one of three colours (red, green, blue) for the message in 'Status' to\
        indicate type of info.
    (2017/03/30) Transfer periodic activity from arrow in version-0.3 to status only in 0.4;\
            with further mod. to Status.
        Some attention to the window size, management of 'Next ...' buttons (which is now more\
            critical for the user to understand) and bold text.
    (2017/05/27) Translation possibility in folder "'gimp-user'/plugins/locale" and\
        first French (fr) translation.
    (2017/06/11) Finally I have opted for an error message, in the case of clicked 'Next...'\
        buttons with an empty active layer and with the '(act.)' state for last arrow.
      This close version 0.4.0 .
 Version 0.4.1 (2017/07/24): at beginning of GIMP-2.9.6?
    Tweaking the messages in status if 'Next...' buttons are blocked following the error message\
        and more messages tweak.
    Remember the arrow at closing time and recall if it's resuming, in a new active arrow layer.
    More robust and comprehensive way of resuming; no AC_vectors present or in parasite,\
        is first start.
    'Labelling arrow' with only tail circle (for slider 'Wingsize' = 0): the arrow size is now\
        circle radius, unless 'radius < 1 PX' then 'radius = slider Brush value'.
    (2017/08/11) More precise error message in 'label' and with prompt text markup. Corrected bugs:\
        in 'label', others in 'resuming' after quitting with arrow-layer present and in translation.
        Armouring against damage in installed 'AC_vectors' at launch.
    (2017/09/03) More efficient UI by making the proposed label inside the tail circle of\
        'Labelling arrow'; also make the text on the buttons of the 'Yes_No' pop-up translatable\
         and revised its message.
      Try to keep pop-ups on top window. Add a pop-up message to permit saving before\
        replacing a whole AC_group, in 'resuming_or_not()' and keep translation current.
      Test on GIMP-2.9-6 for Windows and on GIMP-2.8.22 for Linux.
    (2017/10/23) Title for 'Yes_No' pop-ups. Keep the translation current and corrected
        some typos in the French translation.
      Change the colour of dark orange, to improve visibility, and red for '(emp.)'.
    (2017/11/05) Produce a warning if there is a miss-match between PDB and 'pygimp' version.
      Put the empty layer name in the error message, from last actual arrow, which appears\
        in Status.
      Corrected a bug in 'next_error()': should be always an '(emp.)' layer in Status.
      Keep the translation current and a string freeze for this plug-in version.
    (2017/11/18) Now: active layer state in 'Status' have priority; from more to less: are empty,\
        actual and virtual (in line with former decision in version 0.4.0 about error if empty).
      You can resume with a modified 'AC_group' tree, renumbering the name of the greater\
        previous 'AC_arrow #' layer left is automatic and excluding non 'AC_arrow #'.
      Clean-up and simplify some code.
    (2017/12/18) Continue code simplifying.
      Correct a missing '.data' for the parasite, in 'recall_AC_vectors()'.
      Put the 'AC_vector' path at the end of the vector stack instead of at the beginning.
      A new layer-group at the layer stack beginning if the layer-group name is not identical.
 Version 0.4.2 (2017/12/29): for version, 2.8.14 <= GIMP < 3, with pre-registration message.
      Some unfrozen strings that need translation.
      Beside code simplifying, corrected two bugs:
          in 'recall_AC_vectors()', since this vector is no longer at stack beginning;
          in 'resuming_or_not()', should not have removed the second 'if test_bool :'.
    (2018/01/21) Attention to style 4 mostly.
      More tweaking the size of ' Inactive, ' for arrow style 4 to be same length as\
        'Angle of trailing edge (°)' the longer prompt; to have same window size while\
        using the sliders. Greying out this prompt line seem to be the solution.\
        (Following a question by Volker at 'gimpchat.com'.)
      Remove int() and rounding some float, with 2 digits after the decimal point,\
        for on the arrow screen position.
      For this plug-in, a bit Less memory footprint, mostly by less 'import'.
    (2018/02/14) Make the floating precision access to the screen more uniform.
      Corrected a logical bug in 'next_elem_cb()' for style 5.
      Code style more consistent and corrected a typo in an unusual warning message.
      Taking further the prompt 'markup' of slider '#3' but no 'markup' for the other sliders.
      Trace a line, with the foreground colour, around head of style 6.
      A strings freeze for this plug-in version. Should be the beginning of the stable one.
    (2018/02/18) Straightening out usage in 'Status' of '*' (possible label) for style 5:
        by making it only 'self.update_Status_per()' responsibility. Done
      Corrected a bug in 'may_put_label()' for successive, one char, label that was not following\
        the size of the circle (or fixed radius, not considered) and investigate small label.
    (2018/03/03) Sorry too monolithic and big, so brake it in two pieces:
        ArrowsModule.py as imported GUI module (pyc coded, probably faster) and main plug-in is\
        ArrowsCreator-0.4.py. Those two py files goes into the same 'plug-ins' folder while there\
        is one translation for the two files in a sub-folder 'locale'; translation template, like\
        before, is the file 'ArrowsCreator-0.4.pot'.
      The rest concern ArrowsModule.py which have the GUI.
      For the line around head 6, now use an anti-alias brush, it was '1. Pixel' before.
      This won't have much effect (window is iconified): for style 5 status, message missing,\
        in 'next_elem_cb()'.
      Extended the auto sizing in 'may_put_label()' for successive label with a constant number\
        of chars. Can always control the label with GIMP's text tool (but don't use the text-\
        option box on canvas) during the YesNo-PopUp message display.
    (2018/03/17) Bug hunting, some introduce by previous change:
      Bug, need variable 'GIMP_version' in 'resuming_or_not()'.
      In 'arrows_creator()' for closing, corrected a wrong interpretation of the layer 'AC_element'\
        position, should have, in the stack under 'AC_group' after quitting this plug-in.
      Revisiting the translation, trying to keep one '.pot' file with two py files, since it was\
        working before today. While at it change a couple of lines.

====================================================================================================
 License:
    You may use and distribute this plug-in under the terms of the GPL 2 or greater.
    Get the license text at "http://www.gnu.org/licenses/".
"""

import sys, os
import gtk, pygtk
pygtk.require('2.0')
from gettext import install
from ArrowsModule import *


try :
    import gimp
    from gimpfu import *
    from gimpshelf import shelf
except ImportError :
    # launch from a terminal?
    print("Note: GIMP is needed, '%s' is a plug-in for it.\n" % __file__)
    # launch from GUI? use mssgPop(text) in 'ArrowsModule'
    mssgPop("Note: GIMP registering is needed, '%s' is a plug-in for it.\n" % __file__)
    sys.exit(1)

### global variables ###########################################################

### plug-in filename (thanks 'Ofnuts')
whoiam = os.path.abspath(sys.argv[0])
whoiamName = whoiam.split(os.sep)[-1][:-3]

# GIMP PDB version, found at about line 345; pygimp one next
GIMP_version = gimp.version

# initialize internationalization in the user plug-in-locale (even for admin. install?)
# but the user folder can be in Win.: portable or Roaming beside the stable one.
locale_user_dir = os.path.abspath(gimp.directory + os.sep + "plug-ins" + os.sep + "locale")
if not os.path.exists(locale_user_dir) : os.mkdir(locale_user_dir)
install(whoiamName, locale_user_dir, unicode=True)

def sys_file(f_name) :
    """
    filename encoding other than UTF-8 (Windows)
    """
    sys_encoding = sys.getfilesystemencoding()
    if os.name == 'nt' : encoded = f_name.encode(sys_encoding)
    else : encoded = f_name
    return(encoded)

# folder for among other things a config values in user space like 'py_configs'
AC_folder = sys_file(gimp.directory + os.sep + 'py_configs')
# if folder not there, create it. For root install, write folder if in the group
if not os.path.exists(AC_folder) : os.mkdir(AC_folder)

## manage the configuration file
file_shelf = sys_file(AC_folder + os.sep + whoiamName + '_config.txt')  # config(text) file
if os.path.isfile(file_shelf) :
    AC_data = open(file_shelf, 'r')
    AC_argmenu = eval(AC_data.read())
    AC_data.close()
else :
    # prepare the AC_plug-in: Python touch file
    os.utime(whoiam, None)
    # next is for looking at the config file with an text editor
    file_config_head = _("# plug-in menu launcher (string), imagebar menu path (string),")\
        + _(" default_->_style (int), index of the discarded pattern (int):")
    AC_argmenu = [file_config_head, _("Arrows crea_tor ..."),\
        _("/E_xtensions/Plugins-Python/Tools"), 0, 4]  # lint:ok

## to debug mostly on Windows
#if os.name == 'nt':
    #sys.stderr = open("C:/temp/%s-debug.txt"%whoiamName,'a')
    #sys.stderr.write( whoiam.rsplit(os.sep, 2)[1] )
#else:
    #sys.stderr = open("/home/robert/%s-debug.txt"%whoiamName,'a')

#sys.stdout=sys.stderr # So that they both go to the same file

### Plug-in configuration ######################################################

class MenuArrowsCreator_4(gtk.Window) :
    """
    To change plug-in configuration: launching menu and default values at GIMP profile 'py_configs'.

    Now works for a linux-root install (/usr/lib/gimp/2.0/plug-ins), you can copy there\
    this file, but have to set 3 things right! The things are in permissions: EXECUTE,\
    Others=reading only or none, GROUP=<YOUR GROUP> and with ACCESS='READING AND WRITING'.
    Now config is in user space and translation also; independent of where is the plug-in.
    """

    def __init__ (self) :
        gtk.Window.__init__(self)
        self.set_title(_("ArrowsCreator configuration"))
        # The window manager quit signal:
        self.connect("destroy", gtk.main_quit)

        # Make the UI
        self.set_border_width(8)
        vbox = gtk.VBox(spacing=6, homogeneous=False)
        prompt_line = _("  Please configure here, the file '%s' is not there.") % file_shelf\
            + _("\nThe first two entries are the menu placement on the image menu-bar where")\
            + _(" you want it.\nButton OK produces the file; after this window will no longer")\
            + _(" appear if it's there.\n\n  If you restores its config file from the")\
            + _(" trash-can or changes with a text editor, proceed like any plug-in before ")\
            + _("restarting GIMP for a new menu placement.\nBut a way to reconfiguration is")\
            + _(" to remove the previous '..._config.txt' before starting GIMP.\n")\
            + _("  This is ArrowsCreator-0.4 for GIMP version between 2.8.14 and 3.")
        self.label = gtk.Label(prompt_line)
        vbox.add(self.label)

        separator = gtk.HSeparator()
        vbox.add(separator)
        length_lst = len(AC_argmenu)
        label_lst = [_("launcher name = "), _("menu path = <image>"),
            _("default arrow style number = "), _("pattern index for the head FC (colour) = ")]
        entry_lst = [gtk.Entry(max=100), gtk.Entry(max=100), gtk.SpinButton(gtk.Adjustment\
            (0, 0, 6, 1)), gtk.SpinButton(gtk.Adjustment(0, 0, 58, 1))]
        tooltip_lst = [_("Change or/and choose an accelerator key ")\
          + _("by inserting one or \ndisplacing an '_' before the accelerated letter."),
            _("Edit this partial menu path to your liking."),
            _("Choose the beginning arrow style."),
            _("Choose which pattern index to reserve for the head foreground colour-fill.")]
        # rows number in the following table depends of the return list.
        table = gtk.Table(rows=length_lst, columns=2, homogeneous=False)
        table.set_col_spacings(10)
        vbox.add(table)
        self.entry = []
        for ro in range(1, length_lst) :
            # menu path entry and values
            label = gtk.Label(label_lst[ro - 1])
            label.set_alignment(xalign=0.0, yalign=1.0)
            table.attach(label, 0, 1, ro - 1, ro, xoptions=gtk.FILL, yoptions=0)
            self.entry.append(entry_lst[ro - 1])
            if ro < 3 : self.entry[ro - 1].set_text(AC_argmenu[ro])
            else : self.entry[ro - 1].set_value(AC_argmenu[ro])
            self.entry[ro - 1].set_has_tooltip(True)
            self.entry[ro - 1].set_tooltip_text(tooltip_lst[ro - 1])
            table.attach(self.entry[ro - 1], 1, 2, ro - 1, ro)

        separator = gtk.HSeparator()
        vbox.add(separator)

        hbox = gtk.HBox(spacing=5)
        self.btnc = gtk.Button(_("OK"))
        self.btnc.set_has_tooltip(True)
        self.btnc.set_tooltip_text(_("If instead this window is cancel the ")\
            + _("default will be used."))
        self.btnc.connect("pressed", self.press_ok)
        hbox.add(self.btnc)

        vbox.add(hbox)
        self.add(vbox)

        self.show_all()
        return

    def press_ok(self, data=None) :
        """
         AC_argmenu is the link from 'MenuArrowsCreator_4' to ArrowsCreator
        """
        global AC_argmenu
        AC_argmenu = [file_config_head, self.entry[0].get_text(), self.entry[1].get_text(),\
             int(self.entry[2].get_value()), int(self.entry[3].get_value())]
        self.btnc.connect("released", gtk.main_quit)
        self.destroy()

if not os.path.isfile(file_shelf):
    # message for incompatible GIMP version; use a yes/no buttons
    if GIMP_version < (2, 8, 14) or GIMP_version > (2, 11) :
        mess1 = _("FROM pre-registration of ArrowsCreator:\nnote that (2, 8, 14) <= GIMP < ")\
          + _("(3, 0, 0) is needed for the expected brush behaviour, among other things.")\
          + _("\nYour version read as %s . Should replace '%s' ") % (str(GIMP_version), whoiam)\
          + _("with ArrowsCreator-0.2.2 or update GIMP if less than 3.\nIf you want")\
          + _(" to try register it with GIMP anyway, click on Yes.")
        if YesNoPop(_("What pygimp version?"), mess1) != gtk.RESPONSE_YES : sys.exit(1)

    # next is the UI for the user configuration (menu-path input, etc...)
    MenuArrowsCreator_4()
    gtk.main()

    # create and write in ArrowsCreator configuration file
    AC_f = open(file_shelf, 'w')
    AC_f.write(repr(AC_argmenu))
    AC_f.close()

### Main procedure #############################################################

def arrows_creator(image, layer) :
    """
    This is the procedure that is registered with GIMP
    """
    global AC_argmenu, GIMP_version

    # GIMP version from the PDB, but tuple as from pygimp
    pdb_version = pdb.gimp_version().split('.')  # here version is a string
    pdb_version = tuple([int(item) for item in pdb_version])
    if pdb_version != GIMP_version and (pdb_version < (2, 8, 14) or pdb_version > (2, 11)) :
        gimp.message(_("WARNING: your PDB version is '%s', so different from the pygimp one '%s'")\
            % (str(pdb_version), str(GIMP_version)) + _(" and a miss-match!"))
        # officially
        GIMP_version = pdb_version

    ## next was for the case of a size change by explanation of the label?
    #wdth = image.width
    #hght = image.height

    # with gimpshelf avoid duplicate launch (comment out 'shelf' for dev.)
    if shelf.has_key(whoiamName) and shelf[whoiamName] :
        gimp.message(_("ERROR: an 'arrows creator' instance is already running!"))
        return

    ##1) Preparations
    # ********************************************
    shelf[whoiamName] = True
    # the context antialias is set by default in GIMP!

    # instability of GIMP-2.6 core with 'image.undo_group' here but work in 2.8
    image.disable_undo()
    # initial paths?
    vectors_new = []
    init_paths = image.vectors
    if init_paths :
        for p in init_paths :
            # if "AC_vectors" there keep it visible
            if p.name == _("AC_vectors") :
                p.visible = True
                pdb.gimp_image_lower_item_to_bottom(image, p)
                pdb.gimp_image_set_active_vectors(image, p)
            else : p.visible = False
    # configure pattern for the head
    previous_pattern = pdb.gimp_context_get_pattern()
    pdb.gimp_context_set_pattern(pdb.gimp_patterns_get_list('')[1][AC_argmenu[4]])
    # set brush for the shaft explanation of the label
    previous_brush = pdb.gimp_context_get_brush()
    pdb.gimp_context_set_brush("2. Hardness 100")
    pdb.gimp_context_set_dynamics("Dynamics Off")

    ##2) Main event: GUI in 'ArrowsModule.py'
    # ********************************************
    objct = ArrowWindow(image, AC_argmenu[3], AC_argmenu[4], GIMP_version)
    gtk.main()

    ##3) Closing
    # ********************************************
    # restore some context
    pdb.gimp_context_set_brush(previous_brush)
    pdb.gimp_context_set_pattern(previous_pattern)

    if image in gimp.image_list() :
        # cleanup buffer path
        if len(image.vectors)>2 :
            buf_name = pdb.gimp_item_get_name(image.vectors[1])
            if buf_name == _("AC buffer") :
                pdb.gimp_image_remove_vectors(image, vectors_new)

        Lgroup = pdb.gimp_image_get_layer_by_name(image, _("AC_group"))
        if Lgroup :
            image.active_layer = Lgroup
            # quitting go here also
            layer = pdb.gimp_image_get_layer_by_name(image, _("AC_element"))
            if objct.arrow_done and layer :
                position = pdb.gimp_image_get_item_position(image, layer)
                if position == 0 :
                    image.merge_down(layer, 1)
            elif not (objct.arrow_done) and not (objct.layer_miss) :
                # cleanup layer, if close before the arrow is drawn
                image.remove_layer(Lgroup.children[0])
                # remove empty AC group layer
                empty_group = Lgroup and Lgroup.children == []  # empty group
                if empty_group : image.remove_layer(Lgroup)

        image.enable_undo()

        # permitting the user to keep tab on measuring arrow(s), not if last before quitting
        if objct.measurements :
            cur_name = image.name
            mess_txt = _("MEASURING ARROW in %s: \n\n Nr    Size") % cur_name\
                    + _("    Direction (clockwise +)\n")
            for arrow in objct.measurements :
                mess_txt += "  %s  %.1f px   \t %.1f°\n" % (str(arrow[0]) + '.' +\
                                    str(arrow[1]), arrow[2], arrow[3])
            gimp.message(mess_txt)

    shelf[whoiamName] = False

### GIMP registering ###########################################################

register(
         "arrows_creator",  # proc-def in pluginrc
         _("Draw interactive arrows based on a path with two anchors.")\
             + _("\nFrom: ") + whoiam,
         "Draw an arrow following the current path anchors, updating if an "\
             + "arrow control button is pressed.",
         "Akkana Peck, R. Brizard",
         "(c) Robert Brizard",
         "2011",
         AC_argmenu[1],                      # "Arrows crea_tor...",
         "*",
         [
         (PF_IMAGE, "image", "IMAGE:", None),
         (PF_DRAWABLE, "layer", "DRAWABLE:", None)
         ],
         [],
         arrows_creator,
         menu = "<Image>" + AC_argmenu[2],   # "/Extensions/Plugins-Python/Tools"
         domain = (whoiamName, locale_user_dir)
        )
main()
