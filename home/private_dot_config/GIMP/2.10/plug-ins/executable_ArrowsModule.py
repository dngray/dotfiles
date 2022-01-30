#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, pygtk
pygtk.require('2.0')
import pango
from time import strftime
from gobject import timeout_add, source_remove
from gimpfu import *

### Helper functions ###########################################################

def get_all_layers(parent) :
    """
    Layers traversal for GIMP > 2.7, but work also for 2.6 .
    Get all layers recursively from 'parent', either an layer or a GroupLayer.
    Proceeds depth-first. From 'Seldom Needy'
    """
    container = []
    try : layers = parent.layers
    except : return container
    # except: usually means 'parent' has no layers

    for layer in layers :
        container.append(layer)
        if hasattr(layer,"layers") :
            container.extend(get_all_layers(layer) )
    return container

def mssgPop(mess) :
    """
    Pop a markup message
    """
    flag = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
    msgBox = gtk.MessageDialog(None, flag, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, None)
    msgBox.set_markup(mess)
    msgBox.set_keep_above(True)
    msgBox.run()
    msgBox.destroy()

def YesNoPop(title, mess) :
    """
    Pop a 'yes-no' markup question
    """
    flag = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
    msgBox = gtk.MessageDialog(None, flag, gtk.MESSAGE_QUESTION, gtk.BUTTONS_NONE, None)
    # to have translation on button text
    msgBox.add_buttons(_("Yes"), gtk.RESPONSE_YES, _("No"), gtk.RESPONSE_NO)
    msgBox.set_title(title)
    msgBox.set_markup(mess)
    msgBox.set_keep_above(True)
    answer = msgBox.run()
    msgBox.destroy()
    return answer

### GUI integration #########################################

#__metaclass__ = type
class ArrowWindow(gtk.Window) :
    """
    The interactive GUI interface to orchestrate this script
    """

    # for missing item (user error)
    layer_miss = False
    # to detect if an arrow was drawn
    arrow_done = False
    measurements = []
    # pointing with vectors
    init_paths = []

    def __init__ (self, img, style_def, FG_head, GIMP_version) :

        ## define some self variables
        self.img = img
        self.style_def = style_def
        self.FG_head = FG_head
        self.GIMP_version = GIMP_version

        self.IMG_TYPE = 2 * (self.img.base_type) + 1    # layer type with alpha
        # Start of arrow info in 'Status'
        self.sta_stub = _("<b>Element %d%s, arrow %d:</b> ")  # where first %s is '*' or ' '
        self.segment_asterix = ' '  # asterisk indicate label possibility in 'self.sta_stub'
        # arrow controls & 'Next...' actions inactive
        self.warn_stub = _("<b>Path installation</b>, arrow inactive: ")

        self.x1, self.y1, self.x2, self.y2 = 0.0, 0.0, 0.0, 0.0
        self.sliders = {'wingSize' : 60.0 ,     # side of the winghead in PX
                        'wingAngle' : 25.0 ,    # from arrow direction to the edge in °
                        'brush' : 11.0 ,        # brush radius size
                        '#3' : 0.0 }            # * dependent on arrow style
        self.miss = True        # encounter only once a missing element & cut thread
        self.Lgroup = 0         # title Layer-Group
        self.style4_act = True  # flag of slider3 for style 4
        self.deg = "°"          # necessary for translation
        T_angle = _("Angle of trailing edge (%s)\n") % self.deg
        self.H_active = T_angle + _("from arrow direction")
        self.C_shaft = _("Tail circle (radius, PX)\n")
        self.G_shaft = _("Gradient in shaft\n")
        self.head_flag = False

        # for labelling arrow (style 5)
        self.style5_cr = 0        # counter for tail char to merge
        self.pre_char = 0         # last label used, 0 is no label
        self.style5_flag = False  # flag for label business
        self.text_flag = False    # flag for AC text layer
        self.label_cr = 0         # counter for label in XCF file
        self.pre_quotient = 1.0

        # for function 'resuming_or_not()'

        # preparation for function 'update_Arrow()'
        self.start_flag = False   # the anchors are set if True
        self.direct = True        # arrow from first point to second if True
        self.arrow_cr = 1         # AC layer arrow number, value 1 is for start
        self.next_flag = ""

        # for function 'update_Status_per()'
        self.errors_m = [_("image"), _("AC group-layer"), _("layer at least"),\
            _("path at least"), "part for debugging"]
        self.index_state = 1      # integer for self.states message
        self.segment_cr = 1       # segment counter
        self.arrow_cr = 1         # arrow counter
        self.l_arrow = 0.1        # arrow or 'path' length
        self.theta = 0            # arrow orientation or 'path', angle in °
        self.pre_values = "\n"
        self.pre_arrow = []       # arrow in relation to previous
        self.is_virtual = False   # False is actual arrow at that path position

        # for function 'next_error()'
        self.action_flag = False  # for the right status in blocked next action
        self.next_error_mes = ""  # message in next_error() proc.

        self.parasite_txt = "last element(length, orientation, style, start coords)"\
            + ": %f, %f, %.0f, %.1f, %.1f"
        self.title_line = _("ArrowsCreator-0.4")

        ### Make the User-Interface (UI)
        gtk.Window.__init__(self)
        self.set_title(_("Arrows plug-in for GIMP"))
        self.set_keep_above(True)  # keep the window on top when it looses focus__init__(self)

        # The window manager quit signal:
        self.connect("destroy", gtk.main_quit)   # self.quit_destroy

        self.set_border_width(10)
        vbox = gtk.VBox(spacing=6, homogeneous=False)
        self.add(vbox)

        ## on line center, title line in big chars.
        label = gtk.Label(self.title_line)
        label.set_use_markup(True)
        # Change attributes of the label first line: 'self.title_line'
        attr = pango.AttrList()
        title_len = len(self.title_line)
        fg_color = pango.AttrForeground(0, 0, 65535, 0, title_len)
        bg_color = pango.AttrBackground(52000, 52000, 3000, 0, title_len)
        size = pango.AttrSize(17000, 0, title_len)
        bold = pango.AttrWeight(pango.WEIGHT_ULTRABOLD, 0, title_len)
        attr.insert(fg_color)
        attr.insert(bg_color)
        attr.insert(size)
        attr.insert(bold)
        label.set_attributes(attr)
        vbox.add(label)

        ## the prompt for resuming or first start
        self.label = gtk.Label(self.resuming_or_not())
        self.label.set_use_markup(True)
        # Change attributes of the label
        attr = pango.AttrList()
        size = pango.AttrSize(17000, 0, 3)
        attr.insert(size)
        self.label.set_attributes(attr)
        vbox.add(self.label)

        # Verifies that layer start at #1, not the case if we close and resume later
        if self.arrow_cr > 1 :
            # recall self.pre_arrow from parasite
            self.get_pre_layer_parasite()
        # with image type for self.layer
        self.layer = gimp.Layer(img, _("AC_arrow #") + str(self.arrow_cr), self.img.width,\
            self.img.height, self.IMG_TYPE, 100, NORMAL_MODE)    # RGBA_IMAGE
        pdb.gimp_image_insert_layer(self.img, self.layer, self.Lgroup, 0)

        separator = gtk.HSeparator()
        vbox.add(separator)

        table = gtk.Table(rows=3, columns=2, homogeneous=False)
        table.set_col_spacings(10)
        vbox.add(table)

        ## The sliders:
        # Arrowhead size
        label = gtk.Label(_("Arrowing size (PX)"))
        label.set_alignment(xalign=0.0, yalign=1.0)
        label.set_has_tooltip(True)
        label.set_tooltip_text(_("GIMP's pattern index: ") + str(self.FG_head)\
            + _(", causes a foreground colour-fill (default), The rest is for an active ")\
            + _("pattern-arrow-head-fill (GIMP keyboard 'Shift+Ctrl+P')."))
        table.attach(label, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=0)
        adj = gtk.Adjustment(self.sliders['wingSize'], 0.0, 200.0, 0.5)
        adj.connect("value_changed", self.group_slider_cb, 'wingSize')
        scale = gtk.HScale(adj)
        scale.set_digits(1)
        scale.set_round_digits(1)
        scale.set_has_tooltip(True)
        scale.set_tooltip_text(_("distance from arrow point to side corner; arrow head ")\
            + _("side 0 means no head"))
        table.attach(scale, 1, 2, 0, 1)

        # Arrowhead angle
        label = gtk.Label(_("Arrowing angle (%s)") % self.deg)
        label.set_alignment(xalign=0.0, yalign=1.0)
        table.attach(label, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=0)
        adj = gtk.Adjustment(self.sliders['wingAngle'], 1.0, 80.0, 0.5)
        adj.connect("value_changed", self.group_slider_cb, 'wingAngle')
        scale = gtk.HScale(adj)
        scale.set_digits(1)
        scale.set_round_digits(1)
        scale.set_has_tooltip(True)
        scale.set_tooltip_text(_("angle of a head wing distance in relation")\
                    + _("\nto head direction"))
        table.attach(scale, 1, 2, 1, 2)

        # Arrowshaft width
        label = gtk.Label(_("Brush size (radius,PX)"))
        label.set_alignment(xalign=0.0, yalign=1.0)
        label.set_has_tooltip(True)
        label.set_tooltip_text(_("GIMP's brush here, it's about the arrow-shaft.\n")\
            + _("Choose your brush with GIMP 'Shift+Ctrl+B'."))
        table.attach(label, 0, 1, 2, 3, xoptions=gtk.FILL, yoptions=0)
        adj = gtk.Adjustment(self.sliders['brush'], 1, 35, 1.0, 5.0)
        pdb.gimp_context_set_brush_size(2*self.sliders['brush'] + 1)
        adj.connect("value_changed", self.group_slider_cb, 'brush')
        scale = gtk.HScale(adj)
        scale.set_digits(1)
        scale.set_round_digits(1)
        scale.set_has_tooltip(True)
        scale.set_tooltip_text(_("control the shaft thickness."))
        table.attach(scale, 1, 2, 2, 3)

        # Fourth variable (slider) to be change by self.combo_box
        self.label3 = gtk.Label(_("Gradient in shaft"))
        self.label3.set_use_markup(True)
        if self.choice_i > 4 : self.label3.set_label(_("Tail circle (radius,PX)"))
        elif self.choice_i == 4 : self.label3.set_label(self.H_active)
        self.label3.set_alignment(xalign=0.0, yalign=1.0)
        table.attach(self.label3, 0, 1, 3, 4, xoptions=gtk.FILL, yoptions=0)
        self.adj = gtk.Adjustment(self.sliders['#3'], self.a3min, self.a3max, 0.5)
        self.adj.connect("value_changed", self.group_slider_cb, '#3')
        self.adj.connect("changed", self.slider3_lim)
        scale = gtk.HScale(self.adj)
        scale.set_digits(1)
        scale.set_round_digits(1)
        scale.set_has_tooltip(True)
        scale.set_tooltip_text(_("the adjustment purpose and prompt change according ")\
            + _("to the arrow state"))
        table.attach(scale, 1, 2, 3, 4)

        table = gtk.Table(rows=1, columns=2, homogeneous=False)
        table.set_col_spacings(5)
        vbox.add(table)

        ## Make a combo-box for arrow options,
            # fourth slider control the shaft gradient
        choices = [_("Assegai style"),
                   _("Square cut shaft"),
                   _("Measuring arrow"),
                   _("Notched arrow"),
            # fourth slider control the shape of the head wing
                   _("Swept wings with disk joint"),
            # from here fourth slider control the radius of a tail circle
                   _("Labelling arrow"),
                   _("Stroke path and path head")]

        # shaft only if choice is with head=0, head only if head length greater than arrow
        vbox2 = gtk.VBox(spacing=8)
        vbox2.set_border_width(10)
        vbox.pack_start(vbox2)
        self.combo_box = gtk.combo_box_new_text()
        # replacement 'gtk.ComboBoxText()' (GTK: 2.24)?
        self.combo_box.set_wrap_width(1)
        for i in range(len(choices)) :
            self.combo_box.append_text("%d- %s" % (i, choices[i]))
        self.combo_box.set_active(self.choice_i)
        self.combo_box.set_has_tooltip(True)
        self.combo_box.set_tooltip_text(_("choice of arrow style"))
        self.combo_box.connect("changed", self.choice_i_cb)
        table.attach(self.combo_box, 0, 1, 0, 1)

        # toggle arrow direction
        rbtn = gtk.CheckButton(_("Invert"))
        rbtn.connect("toggled", self.arrowDirection_cb, None)
        rbtn.set_has_tooltip(True)
        rbtn.set_tooltip_text(_("inverse arrow direction"))
        table.attach(rbtn, 1, 2, 0, 1)

        ## button for redrawing an arrow already drawn to a new place or ...
        hbox1 = gtk.HBox(spacing=10)
        btn = gtk.Button(_("Redraw the above arrow"))
        btn.connect("pressed", self.redraw_arrow_cb)
        btn.set_has_tooltip(True)
        btn.set_tooltip_text(_("After you finished dragging the path of an active arrow, ")\
            + _("or other GIMP changes and possibly before plug-in 'Next ...' buttons."))
        hbox1.add(btn)
        vbox2.add(hbox1)

        ## Status frame: show the actual arrow info
        span_stat = "<span foreground='blue' background='yellow' weight='bold' >%s</span>"
        label4 = gtk.Label(span_stat % _("Status"))
        label4.set_use_markup(True)

        info_frame = gtk.Frame()
        info_frame.set_label_widget(label4)
        info_frame.set_label_align(0.5, 0.5)
        vbox.pack_start(info_frame, padding=3)
        vbox3 = gtk.VBox(False, 0)

        # marked up with the Pango text markup language: ./pygtk-2.24.0/docs/html\
            # /pango-markup-language.html
        self.span = ["<span foreground='red' background='light grey'>%s</span>",  # 0 red: prob.
            "<span foreground='blue' background='light grey'>%s</span>",          # 1 blue: info
            "<span foreground='dark green' background='light grey'>%s</span>",    # 2 green: OK
            "<span foreground='#804000' background='light grey'>%s</span>",    # 3 burnt orange:att.
            "<span foreground='light grey' background='#858585'>%s</span>"]       # 4 grey out

        self.states = [self.span[1] % _("start, waiting for two anchors  "),       # 0  blue
                       self.span[2] % _("OK, can edit arrow  "),                   # 1  green
                       self.span[0] % _("open the path (try Back-Space)  "),       # 2  red
                       self.span[1] % _("select anchor left there + add one.\n")\
                         +self.span[1] % _("OK if path re-appears "),              # 3  blue
                       self.span[1] % _("move anchor to desired location "),       # 4  blue
                       self.span[0] % _("anchor outside canvas! Drag it inside."), # 5  red
                       self.span[0] % _("extra anchor(s) (try Back-Space)"),       # 6  red
                       self.span[0] % _("needs path tool selected        "),       # 7  red
                       self.span[1] % _("continue, needs a last anchor   "),       # 8  blue
                       self.span[0] % _("no anchor left, put them back!  "),       # 9  red
                       # next needs to be changed, after the extended sizing?
                       self.span[1] % _("size proposed is for one character label.\n")\
                         +self.span[1] % _("   For two subtract 15% or more."),    # 10 blue
           #self.span[1] % _("size is for the proposed label. You can always test\n")\
           #+ self.span[1] % _(" size particularly if number of char changed."),  # 10 blue
                       self.span[0] % _("ERROR on '%s', put an arrow on the layer\n")\
                         +self.span[0] % _(" '%s' and re-click button; or 'Close'!"), #11 red
                       self.span[3] % _("layer stoked, active layer is now empty."),  #12 orange
                       self.span[1] % _("style_2 don't depend on direction "),       # 13 blue
                       self.span[4] % T_angle + _("<b> Inactive, no wing...</b>"),    # 14 grey out
                       self.span[3] % (self.C_shaft + _("<b>Max radius %s %.1f PX</b>"))]  #15 orange

        self.act_vir = [self.span[2] % _(" (act.)"),
                        self.span[3] % _(" (vir.)"),
                        self.span[0] % _(" (emp.)")]

        if (not self.start_flag) : start_label = self.warn_stub + self.states[0]
        else :
            start_label = self.sta_stub % (self.segment_cr, self.segment_asterix, self.arrow_cr)\
                + self.states[1]

        self.label2 = gtk.Label(start_label + self.group_mess)
        self.label2.set_alignment(0.0, 0.0)
        self.label2.set_use_markup(True)
        self.label2.set_has_tooltip(True)
        self.label2.set_tooltip_text(_("Info and state of current operation.\n")\
            + _("An element's asterisk indicates label possibility and parenthesis ")\
            + _("after arrow is for it's state.\n\nPrevious is in arrow layer ")\
            + _("one less than above arrow (if element = 1)."))
        vbox3.pack_start(self.label2, False, False, 0)
        info_frame.add(vbox3)

        ## Make the action buttons box
        hbox2 = gtk.HBox(spacing=10)

        btn = gtk.Button(_("Next element"))
        btn.connect("pressed", self.next_elem_cb)
        btn.set_has_tooltip(True)
        btn.set_tooltip_text(_("Preparation: before a click here, make an active arrow, ")\
            + _("and the label after a 'Next element' click for a labelling arrow, to your ")\
            + _("satisfaction. Top layer, under the AC_group, is the plug-in active one.")\
            + _("\n\nAction: if element>1 or label, then merge down the top layer and so")\
            + _(" stock it. Create a new top layer,"))
        hbox2.add(btn)

        btn = gtk.Button(_("Next arrow"))
        btn.connect("pressed", self.next_arrow_cb)
        btn.set_has_tooltip(True)
        btn.set_tooltip_text(_("Preparation: before a click here, make and work on the ")\
            + _("active arrow to your satisfaction, the click will make it inactive. ")\
            + _("No plug-in label possibility here.")\
            + _("\n\nAction: create a new active AC_arrow layer, the previous layer ")\
            + _("has the above arrow and so stock it."))
        hbox2.add(btn)

        self.btnc = gtk.Button(_("Close"))
        self.btnc.connect("pressed", self.press_close_cb)
        self.btnc.set_has_tooltip(True)
        self.btnc.set_tooltip_text(_("Orderly way to exit for resuming with XCF file"))
        hbox2.add(self.btnc)

        vbox.add(hbox2)
        self.show_all()

        ## terminate __init__ with user's anchors for path in 'first start'
        self.source_anchors = timeout_add(200, self.get_user_anchors_per)

    def recall_AC_vectors(self, vectors_paras, len_lst):
        """
        Utility function. Get a save path, in a parasite, on image here.

        Called from 'resuming_or_not()' in __init__
        """
        # remove "AC_vectors" if test_bool == True
        if len_lst :
            pdb.gimp_image_remove_vectors(self.img, self.paths_list[len_lst-1])
        if vectors_paras :
            # vectors_import_from_string  return 2 elements (but call for the arrow_path)
            pdb.gimp_vectors_import_from_string(self.img,\
                vectors_paras.data.split(', ')[0], -1, False, True)
            return True
        else :
            # plug-in was not closed in previous launch (no parasite)
            gimp.message(_("WARNING: installed path AC_vectors was not saved")\
                + _(" and is damaged!\nSo no resuming."))
            return False

    def manage_arrow_layers(self, child_lst):
        """
        Utility function to renumber some arrow layer(s) if changed by user, for arrow\
         pre-style, in 'AC_group' layers and make non-visible layer that are not\
         _("AC_arrow #").
        Return: message for the prompting with the total number of arrow layer(s)

        Called by 'resuming_or_not()' at about line 565
        """

        # to manage the arrow layers
        tmp_nr = len(child_lst)
        alst = []
        grea_nr = [-1, -1]
        next_gr = [-1, -1]  # [arrow #, index i]
        for i in range(tmp_nr) :
            stringy = child_lst[i].name
            part_cnt = stringy.count(_("AC_arrow #"))
            if part_cnt == 0 :
                # remove visibility here
                child_lst[i].visible = False
                alst.append(i)

            # find the greatest arrow number and next one
            else :
                part_nr = stringy.partition(_("AC_arrow #"))[2]
                if not part_nr.isdigit() :
                    part_nr = '-1'
                    pdb.gimp_layer_set_name(child_lst[i], _("AC_arrow #") + part_nr)
                else :
                    arro_nr = int(part_nr)
                    if arro_nr > grea_nr[0] :
                        next_gr = grea_nr
                        grea_nr = [arro_nr, i]
        non_nr = len(alst)
        total_nr = tmp_nr - non_nr
        if total_nr > 0 :
            # renumber the greater arrow layer
            if grea_nr[0] != -1 :
                pdb.gimp_layer_set_name(child_lst[grea_nr[1]], _("AC_arrow #") + str(total_nr))
        if total_nr > 1 :
            # renumber the next arrow layer
            if next_gr[0] != -1 :
                pdb.gimp_layer_set_name(child_lst[next_gr[1]], _("AC_arrow #") + str(total_nr - 1))
            # and raise the greater to top of stack to be the previous layer
            self.img.raise_layer_to_top(child_lst[grea_nr[1]])
        number = 0
        if non_nr and (grea_nr[0] != -1) :
            child_lst = self.Lgroup.children

            # place non arrow layer(s) at bottom of the image. (in a layer-group)
            alst.reverse()
            for j in alst :
                # indices in 'alst' is before raising layer
                if total_nr > 1 and (grea_nr[1] > j) :
                    j += 1
                    number += 1
                # displace it at the bottom of branch stack
                self.img.lower_layer_to_bottom(child_lst[j])
        self.img.active_layer = child_lst[grea_nr[1] - number]
        self.arrow_cr = total_nr + 1
        prompt_mess = _("\nThe previous number of arrow layer(s) was %d .") % total_nr
        return prompt_mess

    def resuming_or_not(self):
        """
        Is there an 'AC_vectors' in image (important for resuming), for the prompting\
            and renumber of the arrow layer(s) if there,
            for arrow style and 'AC_group' decision.

        Called by __init__(...) at about line 160
        """

        # index of default arrow style from config.
        self.choice_i = self.style_def  # 0
        if self.choice_i > 4 :        # styles with circle tail
            self.sliders['#3'] = 50.0 # value of third slider
            self.a3min = 0.0          # initial min. limit for slider#3
            self.a3max = 200.0        # initial max. limit for slider#3
        elif self.choice_i == 4 :     # style with variable shape head
            self.sliders['#3'] = 90.0
            self.a3min = 50.0
            self.a3max = 140.0
        else :                        # styles with gradient choice
            self.sliders['#3'] = 0.0
            self.a3min = -25.0
            self.a3max = +25.0

        day_time = strftime("%a, %d %b %Y %H:%M")
        self.group_mess = _("\nAC_group: started on ") + day_time

        # is there an _('AC_group') layer present
        self.Lgroup = pdb.gimp_image_get_layer_by_name(self.img, _("AC_group"))
        if self.Lgroup :  # make the AC_group active
            pdb.gimp_image_set_active_layer(self.img, self.Lgroup)

        ## resume if "AC_vectors" is there or available
        self.paths_list = self.img.vectors
        len_lst = len(self.paths_list)
        # in this plug-in '##1) Preparation' path is visible and at the path stack bottom
        AC_vec_bool = len_lst and self.paths_list[len_lst - 1].name == _("AC_vectors")
        test_bool = AC_vec_bool and self.Lgroup
        # or is "AC_vectors" available in parasite?
        vectors_paras = self.img.parasite_find('AC_vectors-path')

        if test_bool :
            anchor_left = True
            # adress the PROB. of anchors remove between usage and included in path parasite
            try : anchors_path = self.paths_list[len_lst - 1].strokes[0].points
            except :
                # no anchor left so damage, but is there an image parasite 'AC_vectors-path'
                anchor_left = False
                test_bool = self.recall_AC_vectors(vectors_paras, len_lst)

            if anchor_left :
                points_coord = anchors_path[0]
                if (points_coord is None or len(points_coord) != 12 or anchors_path[1]) :
                    test_bool = self.recall_AC_vectors(vectors_paras, len_lst)

        if test_bool :
            # the pre-style image parasite if it exist
            style_paras = self.img.parasite_find('prestyle-info')
            if style_paras :
                style_paras_lst = style_paras.data.split(', ')
                self.choice_i = int(style_paras_lst[1])
                if self.choice_i > 4 :        # styles with ellipse tail
                    self.a3min = 0.0          # initial min limit for slider#3
                    self.a3max = 200.0        # initial max limit for slider#3
                elif self.choice_i == 4 :     # style with variable shape head
                    self.a3min = 50.0
                    self.a3max = 140.0
                else :                        # styles with gradient choice
                    self.a3min = -25.0
                    self.a3max = +25.0
                keys = ['wingSize', 'wingAngle', 'brush', '#3']
                for ind in range(2, 6) :
                    self.sliders[keys[ind-2]] = float(style_paras_lst[ind])

            # yes AC_group
            if self.Lgroup.children == [] :           # empty group
                para_txt = _("Started on %s, with GIMP-%s and %s .") % (day_time,\
                    str(self.GIMP_version), self.title_line)
                # replace the group 'layer-info' parasite
                self.Lgroup.attach_new_parasite('layer-info', 1, para_txt)
                prompt_mess = _("\nThe AC_group was empty, refreshing the parasite.")
            else :                                     # group not empty
                child_lst = self.Lgroup.children
                prompt_mess = self.manage_arrow_layers(child_lst)
                # if quit or close after image resizing
                if style_paras and eval(style_paras_lst[0]) :
                    prompt_mess += _(" Since the image may have\nbeen resized ")\
                        + _("by the plug-in if transparent at border; the previous")\
                        + _("\narrow tail coordinates given may be temporary ")\
                        + _("false in 'Status'.")

            # about 75 car. per line in 'self.label'
            prompt_line = \
              _("  <b>Resuming:</b> with a previous path on ")+strftime("%a, %d %b %Y %Hh%M")\
              + _("; to see the\nanchors, <b>select path tool</b> in design mode. ")\
              + prompt_mess\
              + _("\n\n You should move those anchors <b>now</b> and for the rest of this session.")

            # reading layer_group parasite 'label-info' and updating self
            if self.Lgroup and self.Lgroup.children != [] :
                label_paras = self.Lgroup.parasite_find('label-info')
                if label_paras :
                    paras_list = label_paras.data.split(', ')
                    self.pre_char = paras_list[0]
                    self.chara = paras_list[1]
                    self.fontname = paras_list[2]
                    self.font_size = float(paras_list[3])
                    if len(paras_list) == 6 :
                        self.pre_quotient = float(paras_list[4])
                        # next '[:-1]' is for the 0 ending of parasite
                        self.style5_cr = int(paras_list[5][:-1])
                    else : self.style5_cr = int(paras_list[4][:-1])

        # if 'test_bool==False', first start
        else:
            prompt_line = \
              _("  <b>First start:</b> choose colours and <b>select path tool</b> in design mode; place now")\
              + _("\ntwo path anchors (nodes) by clicking at future arrow tail and head on the canvas")\
              + _("\n(avoid closing the path). An arrow should appear, then adjust values in this")\
              + _("\nwindow. See, for more updated info, the <b>'Status'</b> frame below.")\
              + _("\nYou should move those anchors for the rest of the session.")\
              + _("\n\n To change the active arrow colour(s), brush, stroke path, etc... after it's drawn: ")\
              + _("\nchanges it in GIMP and then an arrow <b>redrawing</b>.")

            ## Make a new GIMP group_layer to draw on
            if self.Lgroup :
                if self.Lgroup.children :
                    mess = _("<b>Note:</b> '%s' is running and about to replace") % whoiamName\
                      + _(" the whole existing 'AC_group'!")\
                      + _("\nBefore clicking OK, you can save this file with GIMP.")\
                      + _("\nAfter OK the plug-in window of 'First start' should appear.")
                    mssgPop(mess)

                # remove the old group_layer to have a new AC_vectors
                pdb.gimp_image_remove_layer(self.img, self.Lgroup)
                pdb.gimp_displays_flush()

            self.Lgroup = pdb.gimp_layer_group_new(self.img)
            self.Lgroup.name = _("AC_group")
            self.img.add_layer(self.Lgroup, 0)
            # attach to the new group a 'layer-info' parasite
            para_txt = _("Started on %s, with pygimp-%s and %s .") % (day_time,\
                str(gimp.version), self.title_line)
            self.Lgroup.attach_new_parasite('layer-info', 1, para_txt)

        return prompt_line

    def get_pre_layer_parasite(self):
        """
        Utility function to have the 'self.pre_arrow' list of the active layer.

        Called by __init__(...) at about line 475 and next_arrow_cb()
        """

        # recall self.pre_arrow from parasite
        pre_layer = pdb.gimp_image_get_layer_by_name(self.img, _("AC_arrow #")\
            + str(self.arrow_cr - 1))
        if pre_layer :
            text_paras = str(pre_layer.parasite_find('layer-info'))
        else : text_paras = None
        # parasite template: "last element(length, orientation, style, start coords):"\
            # "%f, %f, %.0f, %.1f, %.1f"
        if text_paras :
            tail_list = text_paras.partition(':')[2].split()
            self.pre_arrow = [float(item[:-1]) for item in tail_list]
            if len(self.pre_arrow) != 5 : self.pre_arrow = []
        else : self.pre_arrow = []

    def arrowDirection_cb(self, rbtn, data=None) :
        """
        Callback from check-button 'direction'
        """
        if not self.start_flag :
            # make 'invert' button temporary inactive
            rbtn.set_active(False)
            return
        if self.choice_i == 2 :
            # measuring arrow don't depend on direction
            rbtn.set_active(False)
            self.update_Arrow()
            # message in Status for explanation
            self.index_state = 13
            return
        self.direct = not self.direct
        self.update_Arrow()

    def group_slider_cb(self, val, param) :
        """
        Grouping of callback() for sliders 'value change'
        """

        if not self.start_flag :
            # block all sliders
            val.set_value(self.sliders[param])
            return
        if self.head_flag and param == '#3' and self.choice_i != 4 :
            # block the slider '#3'
            val.set_value(self.sliders[param])
        elif (not self.style4_act) and param == '#3' and self.choice_i == 4 :
            val.set_value(self.sliders[param])
        else :
            self.sliders[param] = val.value
        if param == 'brush':
            pdb.gimp_context_set_brush_size(2 * self.sliders[param] + 0.5)
        self.update_Arrow()
        return

    def slider3_lim(self, adj) :
        """
        Callback for 'slider3' changed
        """
        adj.set_lower(self.a3min)
        adj.set_upper(self.a3max)
        adj.set_value(self.sliders['#3'])
        # page_size change when size of slider change? not for length of slider

    def choice_i_cb(self, val) :
        """
        Orchestrate the fourth slider with group of arrow style
        """
        # choose the appropriate slider3 for 'self.choice_1'
        previous = self.choice_i
        self.choice_i = self.combo_box.get_active()
        is_grad = previous > 3 and self.choice_i < 4
        is_circ = previous < 5 and self.choice_i > 4
        is_shape = previous != 4 and self.choice_i == 4
        if is_grad :
            self.sliders['#3'] = 0.0
            self.a3min = -25.0
            self.a3max = 25.0
            # for path installation, when no call to self.update_Arrow()
            self.label3.set_label(self.G_shaft)
        elif is_circ :
            self.sliders['#3'] = 50.0
            self.a3min = 0.0
            self.a3max = 200.0
            # label3 prompt set by 'self.group_slider_cb' call, so temporary
            self.label3.set_label(self.C_shaft)
        elif is_shape :
            self.sliders['#3'] = 90.0 # swept angle for triangular head,
            self.a3min = 50.0         # backward swept, lim.=180-self.sliders['wingAngle'],
            self.a3max = 140.0        # forward swept, lim. depends on shaft length?
            self.label3.set_label(self.H_active)
        self.adj.changed()
        # draw the arrow with...
        self.group_slider_cb(self.adj, '#3')

    def redraw_arrow_cb(self, btn) :
        if self.start_flag :
            self.update_Arrow()
        else :
            # path installation
            return

    def get_user_anchors_per(self):
        """
        Keep at it until there are two anchors on the canvas. Group path things here.

        Called from 'timeout_add()' at the end of __init__
        """

        self.paths_list = self.img.vectors
        lst_len = len(self.paths_list)
        try :
            anchors_path = self.paths_list[lst_len - 1].strokes[0].points
            pdb.gimp_item_set_name(self.paths_list[lst_len - 1], "Unnamed")
        except : return True

        # get anchors, 2 anchors with 2 handles each (6 coord. per anchor), in anchors_path[0]
        #   and anchors_path[1] = True if the path is closed.   AC_vectors
        if not (self.start_flag or pdb.gimp_item_get_name(self.paths_list[lst_len - 1]) != \
          "Unnamed") :
            # quit if no image or AC_group or layer
            if (self.img not in gimp.image_list()):
                self.terminate_auto(0)
            elif self.Lgroup not in get_all_layers(self.img):
                self.terminate_auto(1)
            elif self.layer not in self.Lgroup.layers:
                self.terminate_auto(2)

            nr_coord = len(anchors_path[0])
            if nr_coord != 12 or anchors_path[1] :
                # No 2 anchors or path close, no go
                if anchors_path[1] :
                    anchors_path[1] = False
                    # 'update_Status_per() not in operation'
                    self.label2.set_label(self.warn_stub + self.states[2] + "\n")
                elif nr_coord == 6 :
                    self.label2.set_label(self.warn_stub + self.states[8] + "\n")
                else :
                    self.label2.set_label(self.warn_stub + self.states[3])
            else : self.start_flag = True
        else :
            # resume if "AC_vectors" is there
            self.ID_path = self.paths_list[lst_len - 1]
            pdb.gimp_item_set_name(self.ID_path, _("AC_vectors"))
            self.vectors_copy = pdb.gimp_vectors_copy(self.ID_path)
            self.start_flag = True
            source_remove(self.source_anchors)
            self.source_anchors = None
            self.update_Arrow()
            self.source_status = timeout_add(350, self.update_Status_per)
            return False

        return True

    def update_Arrow(self) :
        """
        Start of chain for drawing arrow when their controls (sliders, etc.) changed
         ; check if path components still there.

        Called by the 'redraw_arrow_cb()' or others of the arrow controls box.
        """

        vectors = pdb.gimp_image_get_vectors_by_name(self.img, _("AC_vectors"))
        pdb.gimp_image_set_active_vectors(self.img, vectors)
        try : anchors_path = vectors.strokes[0].points
        # with no anchor left: 'IndexError: list index out of range'
        except :
            # Clear the layer, erasing the old arrow
            self.layer.fill(3)  # 3: (TRANSPARENT_FILL)
            pdb.gimp_displays_flush()
            return
        # check if the anchors are still there
        nr_coord = len(anchors_path[0])
        if nr_coord != 12 or anchors_path[1] :
            # No 2 anchors or path close, no arrow
            return

        # coordinates of first and next anchor
        lastX = nr_coord - 4; lastY = nr_coord - 3
        x1 = round(anchors_path[0][2], 2); x2 = round(anchors_path[0][lastX], 2)
        y1 = round(anchors_path[0][3], 2); y2 = round(anchors_path[0][lastY], 2)

        # check if it's inside the image
        if  min(x1, y1, x2, y2) < 0 or max(x1, x2) > self.img.width or max(y1,\
          y2) > self.img.height :
            return

        # the invert arrow switch
        if self.direct :
            self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        else :
            self.x1, self.y1, self.x2, self.y2 = x2, y2, x1, y1

        self.ID_path.visible = True

        # Clear the layer, erasing the old arrow
        self.layer.fill(3)    # 3: (TRANSPARENT_FILL)

        # next proc. in the chain for setting the new arrow
        self.style_select()
        pdb.gimp_displays_flush()

        self.arrow_done = True
        # to recover from an action freeze in 'next error()'
        self.action_flag = False
        return

    def update_Status_per(self) :
        """
        From the path or arrow; length, angle ,and if previous arrow; \
         periodically (..._per) updated.
        """

        if self.miss :
            # check if image or groupLayer or layer or vector still there, if not exit plug-in
            if (not gimp.image_list()) or (self.img not in gimp.image_list()):
                self.terminate_auto(0)
                return False
            errors = [self.Lgroup not in get_all_layers(self.img),\
                  self.layer not in get_all_layers(self.img),\
                  self.arrow_done and self.ID_path not in self.img.vectors]
            for ind in range(0, 3) :
                if errors[ind] :
                    self.terminate_auto(ind + 1)
                    return False

            vectors = pdb.gimp_image_get_vectors_by_name(self.img, _("AC_vectors"))
            pdb.gimp_image_set_active_vectors(self.img, vectors)
            header0 = self.sta_stub % (self.segment_cr, self.segment_asterix, self.arrow_cr)
            try : anchors_path = vectors.strokes[0].points
            # with no anchor left: 'IndexError: list index out of range'
            except :
                self.label2.set_label(header0 + self.states[9] + "\n")
                return True

            # check if the anchors are still there
                # (prob. with resuming without anchor, self.states[3] stucked?)
            nr_coord = len(anchors_path[0])
            if nr_coord != 12 or anchors_path[1] :
                if anchors_path[1] :
                    self.label2.set_label(header0 + self.states[2] + "\n")
                    vectors.strokes[0].points[1] = False
                elif nr_coord > 12 :
                    self.label2.set_label(header0 + self.states[6] + "\n")
                elif nr_coord < 12 :
                    # put last anchor as active
                    self.label2.set_label(header0 + self.states[3])
                return True

            # coordinates of first and next anchor
            lastX = nr_coord - 4; lastY = nr_coord - 3
            x1 = round(anchors_path[0][2], 2); x2 = round(anchors_path[0][lastX], 2)
            y1 = round(anchors_path[0][3], 2); y2 = round(anchors_path[0][lastY], 2)

            # check if it's inside the image
            if min(x1, y1, x2, y2) < 0 or max(x1, x2) > self.img.width or max(y1,\
              y2) > self.img.height :
                self.label2.set_label(header0 + self.states[5] + "\n")
                return True

            # the invert arrow switch
            if self.direct :
                X1, Y1, X2, Y2 = x1, y1, x2, y2
            else :
                X1, Y1, X2, Y2 = x2, y2, x1, y1

            # computes values for direction
            dy = Y2 - Y1
            dx = X2 - X1
            theta = math.atan2(dy, dx)
            # it gives answer 0 to pi and 0 to -pi considering the signs of dy & dx
            theta_deg = theta * 180.0 / math.pi  # for the user info
            # computes distance tail-head in PX
            if self.choice_i == 5 and self.l_head < 1.0 :
                if self.sliders['#3'] > 1.0 or self.sliders['#3'] == 1.0 :
                    len_arrow = self.radius
                else : len_arrow = self.sliders['brush']
            else : len_arrow = math.hypot(dx, dy)

            self.segment_asterix = ' '
            # find the state of active layer
            if (not self.arrow_done) :
                # color red for empty
                real = self.act_vir[2]
            else :
                if self.choice_i == 5 and self.radius > 13.0 : self.segment_asterix = '*'
                else : self.index_state = 1

                # compare path anchor coords to last arrow
                if [X1, Y1, X2, Y2] == [self.x1, self.y1, self.x2, self.y2] :
                    # same anchors: color dark green for actual
                    if self.next_flag == 'ar_Y' : self.index_state = 1
                    real = self.act_vir[0]
                    self.is_virtual = False
                else :
                    # dragging anchor: color dark orange for virtual
                    real = self.act_vir[1]
                    self.is_virtual = True

            # now put the info in Status
            header1 = _("<b>Element %d%s, arrow %d%s:</b> ") % (self.segment_cr,\
                self.segment_asterix, self.arrow_cr, real)
            if self.index_state == 10 :
                # put a label size message
                self.label2.set_label(header1 + "%.1f px, %.1f°| %s" % (len_arrow, theta_deg,\
                    self.states[self.index_state]))
            elif self.index_state == 11 :
                # error on next buttons
                self.label2.set_label(header1 + " " + self.states[self.index_state]\
                    % (self.next_error_mes, self.layer.name))
            elif self.index_state == 12 :
                # active layer empty
                self.label2.set_label(header1 + " " + self.states[self.index_state]\
                    + self.span[3] % _("\n   So in '%s' what will it be?") % self.layer.name)

            else :
                # status of pre-variables in previous_arrow (updated by buttons 'Next...')
                if (self.pre_arrow and self.pre_arrow[0]) and (self.index_state != 12) :
                    self.pre_values = _("%.3fx , %.2f%s; was style %d at (%.1f, %.1f)px")\
                        % (len_arrow / self.pre_arrow[0], theta_deg - self.pre_arrow[1],\
                        self.deg, int(self.pre_arrow[2]), self.pre_arrow[3], self.pre_arrow[4])
                else :
                    if self.arrow_cr > 1 :
                        self.pre_values = _("no previous in AC_layer #%d!") % (self.arrow_cr - 1)
                    else :
                        self.pre_values = _("no previous")

                self.label2.set_label(header1 + "%.1f px, %.1f°| %s" % (len_arrow, theta_deg,\
                    self.states[self.index_state]) + _("\nRelative to previous: ")\
                    + self.pre_values)
            return True

        # closing 'if self.miss == False :' but should not occur unless debugging
        else :
            # respect of string freeze for 0.4
            mess = " unknown item for 'self.update_Status_per()'"
            print("Missing in %s," % whoiamName + mess)
            self.terminate_auto(mess)
            return False

    def style_select(self) :
        """
        Computes common values for arrow and select which method to call,
          based on arrow type, to draw it.

        Called from the procedure 'update_Arrow()': root of a proc. tree.
        """

        # coords for arrowhead shape: 'points = []'
        # coords for arrow-shaft: self.strokes(start, end)
        self.strokes = [self.x1, self.y1, self.x2, self.y2]

        dy = self.y2 - self.y1
        dx = self.x2 - self.x1
        wingAngleRad = self.sliders['wingAngle'] * math.pi / 180.

        # distance tail-head in PX
        self.l_arrow = math.hypot(dx, dy)
        # arrowhead theoretical length (for the stroke path arrows) and width
        l_head_th = self.sliders['wingSize'] * math.cos(wingAngleRad)
        w_head_th = self.sliders['wingSize'] * math.sin(wingAngleRad)
        self.s_head = 0.0
        # computes values for direction
        theta = math.atan2(dy, dx)
        # it gives answer 0 to pi and 0 to -pi considering the signs of dy & dx
        self.theta = theta * 180 / math.pi  # for the user info

        # call one of head straight or path, return 'points' or 'path_head'
        if self.choice_i < 6 :    # straight
            points = self.head4staigth(theta)
            # if the 3 triangular points are not co-linear, then place a head
            head_bool = self.l_head > 0.0 and points[0][2:4] != points[0][-2:]
            # if swept wings head
            if self.choice_i == 3 :
                head_bool = head_bool and math.hypot(self.x2 - points[0][4], self.y2\
                    - points[0][5]) > 1.0
        elif self.choice_i == 6 :  # path
            self.s_head = l_head_th * w_head_th  # head area
            if self.s_head >= 3.0 :
                path_head = self.head4path(l_head_th)
                head_bool = True    # head_bool: decide if there is an arrowhead
            else : head_bool = False

        # not grey out prompt for slider '#3' other than style 4 (head)
        if self.choice_i < 4 :
            # shaft gradient
            self.label3.set_label(self.G_shaft)
            self.head_flag = False
        elif self.choice_i > 4 :
            # tail circle
            self.label3.set_label(self.C_shaft)
            self.head_flag = False

        # if straight return strokes=coords for shaft, path don't need it but...
        ratio_ha = self.shaft_coord(dx, dy)

        # draw head(s) first--------------------
        if head_bool and self.choice_i == 0 :
            # precaution
            pdb.gimp_selection_none(self.img)
            self.make_head_points(points)

        # draw shaft (if vector diff?) --------------------
        if ratio_ha < 1.0 or not head_bool :

            # length of the gradient cycle wanted in 2.6, not in 2.8?
            four_var = 0
            slider3 = abs(self.sliders['#3'])
            if slider3 > 0 and self.choice_i < 4 :
                # four_var is cycl_grad in shaft, a FLOAT
                four_var = (self.l_arrow - self.l_head) / math.sqrt(slider3)
            elif self.choice_i == 4 :
                # four_var is radius that depends on head width
                four_var = w_head_th
            elif self.choice_i == 5 :
                # four_var is fade in shaft
                four_var = (self.l_arrow - self.l_head) * 1.2     # fade is a FLOAT
            elif self.choice_i > 5 :
                # four_var is radius from slider '#3'
                four_var = self.sliders['#3']
                if self.l_arrow < four_var :
                    self.label3.set_label(self.span[3] % (self.C_shaft + \
                       _("<b>Radius %s %.1f PX</b>") % ('≥', self.l_arrow)))
            funct_dict = {0: self.draw_shaft0, 1: self.draw_shaft1, 2: self.draw_shaft2,\
                          3: self.draw_shaft3, 4: self.draw_shaft4, 5: self.draw_shaft5,\
                          6: self.stroke_shaft6}
            funct_dict.get(self.choice_i)(four_var)
            pdb.gimp_selection_none(self.img)
        else :
            # head only, grey out prompt for slider '#3' other than style 4
            if self.choice_i < 4 :
                # no shaft
                self.label3.set_label(self.span[4] % self.G_shaft + _("no shaft"))
                self.head_flag = True
            elif self.choice_i > 4 :
                # no tail
                self.label3.set_label(self.span[4] % self.C_shaft + _("no tail"))
                self.head_flag = True

        # draw head(s) after (if head diff?)--------------------
        if head_bool :
            # precaution
            pdb.gimp_selection_none(self.img)
            if (self.choice_i < 6 and self.choice_i != 0) :
                self.make_head_points(points)
            elif self.choice_i == 6 : self.make_head_vector(path_head)

        return

    def head4staigth(self, theta) :
        """
        Computes coords of head apexes for straight arrowhead.

         Inputs :   self.x1, self.y1 are arrow tail coordinates
                    self.x2, self.y2 are arrow head coordinates
                    theta is the arrow direction in radian
         Output:    coordinates of the head apexes

        Called from method 'style_select()'
        """

        # 3 apexes head, triangular arrowhead or forward part
        points = []
        aangle = self.sliders['wingAngle'] * math.pi / 180.  # arrowing angle in radian
        dxm = self.sliders['wingSize'] * math.cos(theta - aangle)
        p2x = round(self.x2 - dxm, 1)    # coord x for wingtip 2
        # notation: 'm' is for minus angle and 'p' is for plus
        dym = self.sliders['wingSize'] * math.sin(theta - aangle)
        p2y = round(self.y2 - dym, 1)    # coord y for wingtip 2
        dxp = self.sliders['wingSize'] * math.cos(theta + aangle)
        p3x = round(self.x2 - dxp, 1)    # coord x for wingtip 3
        dyp = self.sliders['wingSize'] * math.sin(theta + aangle)
        p3y = round(self.y2 - dyp, 1)    # coord y for wingtip 3
        points.append([self.x2, self.y2, p2x, p2y, p3x, p3y])
        # actual length of triangular arrowhead in the shaft direction
        self.l_head = math.hypot(self.x2 - (points[0][2] + points[0][4]) / 2.0, self.y2 - (\
                points[0][3] + points[0][5]) / 2.0)

        # 4 apexes head, so add one apex on arrow line
        if self.choice_i == 0 or self.choice_i == 3 :
            if self.choice_i == 0 : shape = 1.5
            else :                  shape = 0.75
            dxa = self.l_head * shape * math.cos(theta)
            dya = self.l_head * shape * math.sin(theta)
            points = []
            points.append([self.x2, self.y2, p2x, p2y, round(self.x2 - dxa, 1),\
                round(self.y2 - dya, 1), p3x, p3y])

        # 5 apexes head, probably the standard; plus two apexes on shaft surface
        # Slider3 is now for swept wing (with 90° = triangular)
        if self.choice_i == 4 :
            shaft2wingtip = self.sliders['wingSize'] * math.sin(aangle) - \
                (self.sliders['brush'] + 0.5)
            if shaft2wingtip < 1.6 :
                # for stake headed, slider3 is inactive
                self.label3.set_label(self.states[14])
                self.style4_act = False
                # head is triangular, so do nothing more
                return(points)
            else :  # forward and backward are inverse?
                self.label3.set_label(self.H_active)
                self.style4_act = True
                # a2: angle between trailing edge and normal to the shaft
                a2 = ((self.sliders['#3'] / 180.) - 0.5) * math.pi
                if a2 == 0. : return((points))
                # a1 is wingtip radian angle for triangular head
                a1 = math.pi * 0.5 - aangle
                l_wingedge = math.hypot(shaft2wingtip, shaft2wingtip * math.tan(a2))
                if -a2 < a1 : self.l_head += l_wingedge * math.sin(a2)
                else :
                    self.l_head = 0
                    return(points)
                # suffix notation: 's' superior and 'i' inferior
                dxs = l_wingedge * math.sin(a2 - theta)
                dys = l_wingedge * math.cos(a2 - theta)
                dxi = l_wingedge * math.sin(a2 + theta)
                dyi = l_wingedge * math.cos(a2 + theta)
                points = []
                points.append([self.x2, self.y2, p2x, p2y,
                       round(p2x - dxs, 1), round(p2y - dys, 1),
                       round(p3x - dxi, 1), round(p3y + dyi, 1),
                       p3x, p3y])

        # double triangular headed
        if self.choice_i == 2 :
            points.append([self.x1, self.y1,
                       round(self.x1 + dxm, 1), round(self.y1 + dym, 1),
                       round(self.x1 + dxp, 1), round(self.y1 + dyp, 1)])
        return(points)

    def head4path(self, l_head_th) :
        """
        Computes path of the head for path arrow.
        Called from method 'style_select()'

        Output:    head closed vectors.
        """
        # very small surface_head eliminate by 'self.style_select()'
        points = []
        if l_head_th < self.l_arrow :
            # stroke length and straight length: 'self.l_arrow'
            length = self.ID_path.strokes[0].get_length(3)
            factor = 1.0 + (length - self.l_arrow) / length

            for repeat in range(2) :
                if self.direct :
                    dist = length - l_head_th * factor
                else :
                    dist = l_head_th * factor
                x_point, y_point, slope = self.ID_path.strokes[0].get_point_at_dist(dist, 2)[:3]
                l_head_new = math.hypot(self.x2 - x_point, self.y2 - y_point)
                if repeat == 0 : factor += (l_head_th - l_head_new) / l_head_th

            sin = (self.y2 - y_point) / l_head_new
            cos = (self.x2 - x_point) / l_head_new
            width_head = l_head_new * math.tan(self.sliders['wingAngle'] * math.pi / 180.)
            deltaX = width_head * sin
            deltaY = width_head * cos
            x1 = x_point + deltaX
            y1 = y_point - deltaY
            x2 = x_point - deltaX
            y2 = y_point + deltaY
            theta = math.atan2(sin, cos)

        else :
            # compute the 'points' for the head by the line from the anchors
            # self.x1, self.y1, self.x2, self.y2 are on the straight line; see head4staigth()
            theta = math.atan2((self.y2 - self.y1), (self.x2 - self.x1))
            aangle = self.sliders['wingAngle'] * math.pi / 180.    # arrowing angle in radian
            dxm = self.sliders['wingSize'] * math.cos(theta - aangle)
            x2 = self.x2 - dxm     # coord x for wingtip 2
            # notation: 'm' is for minus angle and 'p' is for plus
            dym = self.sliders['wingSize'] * math.sin(theta - aangle)
            y2 = self.y2 - dym     # coord y for wingtip 2
            dxp = self.sliders['wingSize'] * math.cos(theta + aangle)
            x1 = self.x2 - dxp     # coord x for wingtip 1
            dyp = self.sliders['wingSize'] * math.sin(theta + aangle)
            y1 = self.y2 - dyp     # coord y for wingtip 1

        points.append([self.x2, self.y2,
                        round(x1, 1), round(y1, 1),
                        round(x2, 1), round(y2, 1)])
        # actual length of arrowhead in the head direction
        self.l_head = math.hypot(self.x2 - (points[0][2] + points[0][4]) / 2.0, self.y2 -\
                 (points[0][3] + points[0][5]) / 2.0) - 0.5

        # construct the head by a close path
        cont_len = self.sliders['wingSize'] * 0.3     # for the C(ontrol) point
        # psi is half value of the 'wingAngle' in radian
        psi = self.sliders['wingAngle'] * math.pi / 360.
        ang1 = math.pi / 2. - theta - psi
        ang3 = math.pi / 2. - theta + psi
        del_x0 = - math.sin(ang1) * cont_len
        del_y0 = - math.cos(ang1) * cont_len
        del_x1 = math.cos(theta) * cont_len
        del_y1 = math.sin(theta) * cont_len
        del_x3 = - math.sin(ang3) * cont_len
        del_y3 = - math.cos(ang3) * cont_len
        vectors1 = pdb.gimp_vectors_new(self.img, 'AC_head6')
        # at wing end C point has the same head_slope (variable?), at the tip C\
        # is an intermediary. Take the points[x] above for the A (anchors) starting\
        # from head tip: CAC clockwise
        pdb.gimp_vectors_stroke_new_from_points(vectors1, 0, 24,
            (self.x2, self.y2, self.x2, self.y2, self.x2 + del_x0, self.y2 + del_y0,
            x1 + del_x1, y1 + del_y1, x1, y1, x1, y1,
            x2, y2, x2, y2, x2 + del_x1, y2 + del_y1,
            self.x2 + del_x3, self.y2 + del_y3, self.x2, self.y2, self.x2, self.y2),
            True)
        pdb.gimp_image_insert_vectors(self.img, vectors1, None, 1)
        vectors1.visible = False

        pdb.gimp_image_set_active_vectors(self.img, self.ID_path)

        return(vectors1)

    def shaft_coord(self, dx, dy) :
        """
        Modify beginning and ending coords for straight arrow shaft.
        Changes four int. (self.strokes) and return a float (ratio)

        Called from style_select()
        """

        # ratio is length_head/length_arrow, if >= 1 no shaft if there is a head
        ratio = self.l_head / self.l_arrow
        if self.choice_i < 6 :
            # don't go all the way to the end for self.choice_i != 3, because of overshoot\
                # of shaft.
            if ratio != 0 and ratio < 1.0 :
                # a head at the end except for notched arrow where shaft is arrowlength
                lcx = ratio * dx
                lcy = ratio * dy
                if self.choice_i != 3 :
                    # from similar triangles
                    self.strokes[2] -= lcx
                    self.strokes[3] -= lcy
                # a head at the beginning
                if self.choice_i == 2 :
                    self.strokes[0] += lcx
                    self.strokes[1] += lcy
                    ratio *= 2.0
            # next is independent of arrow head = 0
            if self.sliders['#3'] < 0 and ratio < 1.0 :
                # inverse gradient: pdb.gimp_context_swap_colors(), not as general?
                self.strokes = [self.strokes[2], self.strokes[3], self.strokes[0], self.strokes[1]]
        return(ratio)

    def draw_shaft0(self, cycl_grad) :
        """
        Arrow shaft is a paintbrush stroke after the head.
        Style 0: Assegai style

        Called from method 'style_select()'
        """

        pdb.gimp_paintbrush(self.layer, 0.0, 4, self.strokes, 0, cycl_grad)
        # put a rivet for fixation at shaft-head
        br_size = pdb.gimp_context_get_brush_size()
        pdb.gimp_context_set_brush_size((2 * self.sliders['brush'] + 1.0) / 3.0)
        if self.sliders['#3'] >= 0 : riv_pt = [self.strokes[2], self.strokes[3]]
        # if no head no rivet?
        else : riv_pt = [self.strokes[0], self.strokes[1]]
        pdb.gimp_paintbrush_default(self.layer, 2, riv_pt)
        pdb.gimp_context_set_brush_size(br_size)
        return

    def draw_shaft1(self, cycl_grad) :
        """
        A selection to square cut the following 'paintbrush' operation.
        Style 1: Square cut shaft

        Called from method 'style_select()'
        """

        width_sel = self.sliders['brush']
        deltaX = width_sel * (self.y2 - self.y1) / self.l_arrow
        deltaY = width_sel * (self.x2 - self.x1) / self.l_arrow
        points_shaft = [self.strokes[2] + deltaX, self.strokes[3] - deltaY,\
                        self.strokes[2] - deltaX, self.strokes[3] + deltaY,\
                        self.strokes[0] - deltaX, self.strokes[1] + deltaY,\
                        self.strokes[0] + deltaX, self.strokes[1] - deltaY]
        # 2: CHANNEL_OP_REPLACE
        pdb.gimp_image_select_polygon(self.img, 2, 8, points_shaft)
        pdb.gimp_paintbrush(self.layer, 0.0, 4, self.strokes, 0, cycl_grad)
        return

    def draw_shaft2(self, cycl_grad) :
        """
        Measuring arrow: X width of shaft, double heads.
        Style 2: Measuring arrow

        Called from method 'style_select()'
        """

        fX = (self.y2 - self.y1) / self.l_arrow
        fY = (self.x2 - self.x1) / self.l_arrow
        # no head above don't produce a shaft so base it on shaft width
        width_sel = self.sliders['brush'] * 1.5
        deltaX = width_sel * fX
        deltaY = width_sel * fY
        points_shaft = [self.strokes[2] + deltaX, self.strokes[3] - deltaY,
                        self.strokes[2] - deltaX, self.strokes[3] + deltaY,
                        # make an X shaft!
                        self.strokes[0] + deltaX, self.strokes[1] - deltaY,
                        self.strokes[0] - deltaX, self.strokes[1] + deltaY]
        # for the arrow centre symmetry: two paint-brush strokes
        x_center = (self.strokes[0] + self.strokes[2]) / 2.0
        y_center = (self.strokes[1] + self.strokes[3]) / 2.0
        # to inverse the gradient
        if self.sliders['#3'] > 0.0 :
            half_stroke1 = [x_center, y_center, self.strokes[0], self.strokes[1]]
            half_stroke2 = [x_center, y_center, self.strokes[2], self.strokes[3]]
        else :
            half_stroke1 = [self.strokes[0], self.strokes[1], x_center, y_center]
            half_stroke2 = [self.strokes[2], self.strokes[3], x_center, y_center]
        # X shaft by that selection
        pdb.gimp_image_select_polygon(self.img, 2, 8, points_shaft)

        pdb.gimp_paintbrush(self.layer, 0.0, 4, half_stroke1, 0, cycl_grad)
        pdb.gimp_paintbrush(self.layer, 0.0, 4, half_stroke2, 0, cycl_grad)
        return

    def draw_shaft3(self, cycl_grad) :
        """
        A selection for notched arrow.
        Style 3: Notched arrow

        Called from method 'style_select()'
        """

        width_sel = self.sliders['brush']

        if self.sliders['#3'] < 0 :
            self.strokes = [self.strokes[2], self.strokes[3], self.strokes[0], self.strokes[1]]
        deltaX = width_sel * (self.strokes[3] - self.strokes[1]) / self.l_arrow
        deltaY = width_sel * (self.strokes[2] - self.strokes[0]) / self.l_arrow
        points_shaft = [self.strokes[2], self.strokes[3],
                        self.strokes[0] - deltaX, self.strokes[1] + deltaY,
                        self.strokes[0] + deltaY * 0.7, self.strokes[1] + deltaX * 0.7,
                        self.strokes[0] + deltaX, self.strokes[1] - deltaY]

        pdb.gimp_image_select_polygon(self.img, 2, 8, points_shaft)
        if self.sliders['#3'] < 0 :
            self.strokes = [self.strokes[2], self.strokes[3], self.strokes[0], self.strokes[1]]
        pdb.gimp_paintbrush(self.layer, 0.0, 4, self.strokes, 0, cycl_grad)
        return

    def draw_shaft4(self, radius) :
        """
        Style 4: Disk joint arrow. Size of disk joint related to head size.

        Called from method 'style_select()'
        """

        cycl_grad = self.l_arrow - self.l_head  # cycl_grad is a FLOAT
        # Look into 'shaft_coord()' for strokes
        pdb.gimp_paintbrush(self.layer, 0.0, 4, [self.strokes[2], self.strokes[3],
                            self.strokes[0], self.strokes[1]], 0, cycl_grad)
        # radius of arrow rotule equal half width of head
        if radius >= 1.0 :
            diameter = round(2.0 * radius, 1)
            px = round(self.strokes[0] - radius, 1)
            py = round(self.strokes[1] - radius, 1)
            pdb.gimp_image_select_ellipse(self.img, 2, px, py, diameter, diameter)
            pdb.gimp_edit_fill(self.layer, 1)   # 1: (BACKGROUND_FILL)
            pdb.gimp_selection_none(self.img)
        return

    def draw_shaft5(self, fade) :
        """
        Style 5: Labelling arrow.
        For version > 0.3.4 a two step affair (arrow and label), here is part of the first.

        Called from method 'style_select()'
        """

        short_shaft = self.l_arrow - self.l_head
        if self.sliders['#3'] < short_shaft :
            self.radius = self.sliders['#3']
            self.label3.set_label(self.C_shaft)
        elif self.sliders['#3'] < 3.3 or short_shaft < 6.5 :
            self.radius = 0.0
        else :
            self.radius = short_shaft
            self.label3.set_label(self.states[15] % ('=', round(self.radius, 1)))

        if self.radius :
            # disk selection and stroke circle
            diameter = round(2.0 * self.radius, 1)
            px = round(self.strokes[0] - self.radius, 1)
            py = round(self.strokes[1] - self.radius, 1)
            self.strokes[0] += self.radius * (self.x2 - self.x1) / self.l_arrow
            self.strokes[1] += self.radius * (self.y2 - self.y1) / self.l_arrow
            pdb.gimp_image_select_ellipse(self.img, 2, px, py, diameter, diameter)

            # restore brush size after the circle stroke
            br_size = pdb.gimp_context_get_brush_size()
            # trace the circle from the selection
            if self.radius < 20.0 :
                pdb.gimp_context_set_brush_size(3.0)
            else :
                pdb.gimp_context_set_brush_size(4.0)    # (brush_name, 1.5)
            pdb.gimp_edit_stroke(self.layer)
            pdb.gimp_selection_none(self.img)
            pdb.gimp_context_set_brush_size(br_size)    # (brush_name, br_radius)

        # put a mark at the circle centre if no radius
        else : pdb.gimp_paintbrush(self.layer, 0.0, 2, self.strokes[:2], 0, 0.0)

        if self.l_head < 1.0 :
            if self.sliders['#3'] >= 1 :
                self.l_arrow = self.sliders['#3']
            else : self.l_arrow = self.sliders['brush']
            return     # for a circle only

        # paint brush for the arrow shaft
        pdb.gimp_paintbrush(self.layer, fade, 4, self.strokes, 0, 0.0)
        return

    def stroke_shaft6(self, radius) :
        """
        The path stroke will be the shaft with foreground colour, the rest (radius and head)\
            with background.

        Called from method 'style_select()'
        """

        if radius :
            # draw the starting disk
            diameter = round(2.0 * radius, 1)
            px = round(self.strokes[0] - radius, 1)
            py = round(self.strokes[1] - radius, 1)
            pdb.gimp_image_select_ellipse(self.img, 2, px, py,\
                diameter, diameter)
            pdb.gimp_edit_fill(self.layer, 1)   # 1: (BACKGROUND_FILL)
            pdb.gimp_selection_none(self.img)
        OP_type = 2
        if self.s_head >= 3.0 :
            # make a selection to stop the stroke at the arrow head
                # (unnecessary for only a head in most case)
            x_head = self.strokes[2] - self.l_head
            y_head = self.strokes[3] - self.l_head
            # if polygon selection use the value of 'self.sliders['brush']' but ...
            #pdb.gimp_image_select_polygon(self.img, OP_type, num_segs, segs)
            pdb.gimp_image_select_ellipse(self.img, OP_type,\
                x_head, y_head, 2.0 * self.l_head - 1.0, 2.0 * self.l_head - 1.0)
            pdb.gimp_selection_invert(self.img)

        # stroke with active brush and foreground colour
        pdb.gimp_edit_stroke_vectors(self.layer, self.ID_path)
        pdb.gimp_selection_none(self.img)
        return

    def make_head_points(self, points) :
        """
        Select and paint the arrowhead shape(s) (or other decorations?)
         'points' is in the form [[6 coords], [6 coords], ...] for triangles.

        Called from method 'style_select()'
        """

        for h in points :
            pdb.gimp_image_select_polygon(self.img, CHANNEL_OP_ADD, len(h), h)

        # Fill the arrowhead(s), PATTERN_FILL work too
        name = pdb.gimp_context_get_pattern()
        # the next is the index pattern used for a foreground_fill
        if name != pdb.gimp_patterns_get_list('')[1][self.FG_head] :   # 4
            # return a number and name list
            pattern = 4      # 4: (PATTERN_FILL)
        else :  pattern = 0  # 0: (FOREGROUND_FILL)
        pdb.gimp_edit_fill(self.layer, pattern)
        pdb.gimp_selection_none(self.img)
        return

    def make_head_vector(self, path) :
        """
        Select and paint the arrowhead shape(s) (or other decorations?)
         'vector' is in close form, (slower than points).

        Called from method 'style_select()', retricted for now to style 6.
        """

        # convert the closed vector to a selection
        pdb.gimp_image_select_item(self.img, CHANNEL_OP_ADD, path)

        pdb.gimp_image_remove_vectors(self.img, path)
        # this made dragging the anchor non smooth?

        # Fill the arrowhead(s), PATTERN_FILL work too
        name = pdb.gimp_context_get_pattern()
        # next is the index pattern used for a foreground_fill
        if name != pdb.gimp_patterns_get_list('')[1][self.FG_head] :   # 4
            # like 'make_head_points()'
            pattern = 4      # 4: (PATTERN_FILL)
        else :  pattern = 1  # 1: (BACKGROUND_FILL)
        pdb.gimp_edit_fill(self.layer, pattern)

        # foreground line around the head, restore brush after the stroke
        br_size = pdb.gimp_context_get_brush_size()
        br_name = pdb.gimp_context_get_brush()
        #'2. Hardness 100' with antialias;   #'1. Pixel' no antialias
        pdb.gimp_context_set_brush("2. Hardness 100")
        pdb.gimp_context_set_brush_size(1.5)
        pdb.gimp_edit_stroke(self.layer)
        # return to previous brush
        pdb.gimp_context_set_brush(br_name)
        pdb.gimp_context_set_brush_size(br_size)

        pdb.gimp_selection_none(self.img)
        return

    def merge_elem(self) :
        """
        Manages for element layer, the previous arrow info.

        Called from 'next_elem_cb(...)' and 'press_close_cb()'
        """

        # check if there is an under layer and merge down
        if len(self.img.layers) > 1 :
            self.img.raise_layer_to_top(self.layer)
            layer = self.img.merge_down(self.layer, 1)
            # for arrow attach parasite
            layer.attach_new_parasite('layer-info', 1, "last element(length,"\
              + " orientation, style, start coords): %f, %f, %.0f, %.1f, %.1f"\
              % (self.l_arrow, self.theta, self.choice_i, self.x1, self.y1))
            # arrow start position: self.x1, self.y1
        else : self.terminate_auto(_("layer to merge with"))
        return

    def may_put_label(self) :
        """
         May put a chosen label inside the tail circle of 'Labelling arrow' and save as
         text-layer if there some text with the label.

         Called from 'next_elem_cb(...)'
        """
        ## for style with tail circle use this to put a label inside the circle.
        self.style5_flag = True
        # place some info in Status? Not the place
        self.index_state = 10

        # create a text-layer: chara = ' ' make the layer creation fail
        if self.style5_cr == 0 :    # counter for tail char to merge
            self.chara = unichr(ord('a'))
            self.pre_char = self.chara
            if self.radius < 20.0 : self.font_size = (self.radius - 4.0) * 1.4
            else : self.font_size = (self.radius - 5.0) * 1.35
        else :
            # subsequent labels, work with many chars
            len_label = len(self.chara)
            try :
                self.chara = self.chara[:len_label - 1] + chr(ord(self.chara[len_label - 1]) + 1)
                self.font_size = self.pre_quotient * self.radius
            except :
                self.chara = unichr(ord('a'))  # re-begin
                if self.radius < 20.0 : self.font_size = (self.radius - 4.0) * 1.4
                else :
                    # pdb.gimp_text_layer_set_font_size(layer, font_size, unit)
                    self.font_size = (self.radius - 5.0) * 1.35

        self.fontname = pdb.gimp_context_get_font()
        charLayer = pdb.gimp_text_layer_new(self.img, self.chara, self.fontname, self.font_size, 0)
        # last is unit: 0 for Pixel and 1 for Point
        pdb.gimp_image_insert_layer(self.img, charLayer, self.Lgroup, 0)

        # put proposed char(s) (with background?) at offset
        width, height = pdb.gimp_text_get_extents_fontname(self.chara,\
            self.font_size, 0, self.fontname)[:2]
        offx = self.x1 - width / 2.0
        offy = self.y1 - height / 2.0
        pdb.gimp_layer_set_offsets(charLayer, offx, offy)

        # promt_line inside a 'yes/no' pop-up
        title = _("   Label for this Labelling arrow?")
        if self.style5_cr == 0 :
            mess1 = _("At this window opening, the font was <b>%s</b>: it affects the proposed ")\
              % self.fontname + _("label size. For a label change read the next paragraph, ")\
              + _("starting with <b>'If needed.'</b> .")
        else :
            mess1 = _("The font is <b>%s</b> and the label number is %d.")\
              % (self.fontname, self.style5_cr + 1)
        mess2 = _("\nIf you answer <b>Yes</b>, try to put a printable label at the centre of the tail circle")\
          + _(" and passes to next arrow.\nIf <b>No</b>, no label and produces a next element.")\
          + _("\n\nIf needed. Then open the <b>Text Tool</b> dialogue with left-click on the tool")\
          + _(" followed by a left-click on the proposed char <b>'%s'</b>, this makes a text-option")%self.chara\
          + _(" box on the image. The master text-options seems the one dock under the tool box, for")\
          + _(" example, to change FG colour (the goal is to be consistent on all).")\
          + _("\nYou select, tweak and keyboard the character(s) of the text layer, on GIMP at the centre of")\
          + _(" the tail circle (move the text-layer with <b>Move Tool</b>, to check the fit).")\
          + _("\nAn explanation of the label is optional, add automatically in a different text layer,")\
          + _(" if it has the separator <b>' :'</b> after the label; the window focus is important.")\
          + _("\nFinally re-select the <b>Path Tool</b> and click on the path.")\
          + _("\n\nProblems are interpreted as answer <b>No</b>.\nYour answer close this window.")
         ##; don't use the canvas text-box

        self.iconify()
        pdb.gimp_displays_flush()
        answer_pop = YesNoPop(title, mess1 + mess2)

        # after the user label answer
        problem = False
        # max length of a label is three bytes now
        max_len = 3
        if pdb.gimp_item_is_text_layer(charLayer) :
            text_layr = pdb.gimp_text_layer_get_text(charLayer)
            # if use the canvas text-box: 'text_layr' has no proper length
            try :
                len_chr = len(text_layr)
                # text_layr must have the focus, if not problem for linux?
                problem = len_chr > max_len and (text_layr.find(' :') > max_len \
                    or text_layr.find(' :') < 1)
            except :
                len_chr = 0
                problem =  True

            # separate the label from the rest with ' :'
            if not problem :
                if len_chr > max_len : self.chara = text_layr[:text_layr.find(' :')]
                elif len_chr < max_len + 1 : self.chara = text_layr
                # to grow the width of the label (affect the 'charLayer' displayed)
                label = ' ' + self.chara + ' '
                pdb.gimp_text_layer_set_text(charLayer, label)

                # for length in unicode char
                self.font_size, unit = pdb.gimp_text_layer_get_font_size(charLayer)
                self.fontname = pdb.gimp_text_layer_get_font(charLayer)
            else : err = _("too long & no label")

            is_nolabel = len_chr < 1 or problem
            if len_chr < 1 : err = _('not printable')
        else :  # no longer an uniform text_layer
            text_layr = None
            is_nolabel = True
            err = _("changed to non text")

        self.deiconify()
        self.style5_flag = False

        if answer_pop == gtk.RESPONSE_YES and not is_nolabel :
            # put label in the circle by offsets
            width, height = pdb.gimp_text_get_extents_fontname(label,\
                self.font_size, unit, self.fontname)[:2]
            offx = self.x1 - width / 2.0
            offy = self.y1 - height / 2.0
            pdb.gimp_layer_set_offsets(charLayer, offx, offy)
            radius = self.font_size * 0.1
            pdb.gimp_image_select_item(self.img, 0, charLayer)
            pdb.gimp_selection_grow(self.img, int(radius))
            pdb.gimp_selection_feather(self.img, radius)
            pdb.gimp_edit_bucket_fill(charLayer, 1, 2, 100, 0, False, 0, 0)
            pdb.gimp_selection_none(self.img)

            self.layer = self.img.merge_down(charLayer, 1)
            # counter of arrow labels (save across session for resuming?)
            self.style5_cr += 1
            # keeping tab on last self.chara
            self.pre_char = self.chara
            self.pre_quotient = self.font_size / self.radius

            # keep the text-layer (Rod Detmer idea)
            if len_chr > max_len :
                # self.fontname= 'sans'?
                Layer_out = pdb.gimp_text_layer_new(self.img, "(AC_label %s)\n"\
                    % self.chara + text_layr, self.fontname, 15, 0)
                pdb.gimp_image_insert_layer(self.img, Layer_out, None,\
                    len(self.img.layers))
                width, height = pdb.gimp_text_get_extents_fontname(text_layr,\
                    15, 0, self.fontname)[:2]
                offx = self.x1 - width / 2.0
                offy = self.y1 - height / 2.0
                pdb.gimp_layer_set_offsets(Layer_out, offx, offy)
                self.text_flag = True
            self.next_arrow_cb()
            return True

        else :
            self.img.remove_layer(charLayer)
            pdb.gimp_displays_flush()

            # if answer_pop == "Yes": error message
            mess = _("ERROR in labelling element %d of AC_arrow #%d")\
                % (self.segment_cr, self.arrow_cr)\
                + _(":\nthe label was not accepted because the text-layer is '%s'!")
            if answer_pop == gtk.RESPONSE_YES  and is_nolabel :
                # problem with edition of char
                gimp.message(mess%err)
            elif answer_pop == gtk.RESPONSE_YES :
                self.style5_cr - 1
                gimp.message(mess%_("unknown"))

            if self.pre_char : self.chara = self.pre_char
            return False

    def terminate_auto(self, reason_index) :
        """
        Leave a message (with problem) and make an unscheduled plug-in termination

        Can be called from thread 'update_Status_per()'.
        """

        if reason_index in [0, 1, 2, 3, 4] : reason = self.errors_m[reason_index]
        else : reason = reason_index
        gimp.message(_("ERROR: a missing %s is undermining this plug-in") % reason\
            + _(".\nIt has been auto terminated!"))
        # the update() function don't stop instantly it seems
        self.miss = False

        if reason_index == 0 :
            self.destroy()
            gtk.main_quit()
            return

        self.layer_miss = True
        # remove empty AC_group layer (if there)
        if reason_index != 1 :
            empty_group = self.Lgroup and self.Lgroup.children == []  # empty group
            if empty_group:
                self.img.remove_layer(self.Lgroup)
        # replace a missing AC_vectors
        if reason_index == 3 :
            pdb.gimp_image_insert_vectors(self.img, self.vectors_copy, None, 0)
            pdb.gimp_item_set_name(self.vectors_copy, _("AC_vectors"))

        if reason_index == 4 :
            self.source_status = None
            self.destroy()
            return  # with self.miss false

        if self.source_status : source_remove(self.source_status)

        self.destroy()
        gtk.main_quit()
        return self.measurements

    def next_error(self) :
        """
        Called by unsuccessful next procedures
        """

        # from last actual arrow: stuck on what?
        if self.next_flag == 'ar_Y' :
            self.next_error_mes = _("Next arrow")
        else :
            self.next_error_mes = _("Next element")
        self.index_state = 11
        # blocked empty (emp.) action, for all last arrow
        self.action_flag = True
        return

    def next_elem_cb(self, btn, data=None) :
        """
        Automate the merge down for this plug-in, with action name & some basic in tooltip.
        May merge also a label for 'Labelling arrow' which is style 5 (self.choice_1=5).

        Callback from action button name 'Next element'
        """

        if (not self.start_flag) : return

        if self.index_state == 12 or not self.arrow_done :
            mess_block = _("<b>stocking blocked</b> by an empty")
        else : mess_block = _("stocked the previous active ")
        # leave trace of last action; about 75 chars per line?
        prompt_line = _("  <b>Next element:</b> this was the last action clicked and ") + mess_block\
        + _("\nlayer. Put many arrows or element in one layer by merging down. Also a chosen label is")\
        + _("\npossible for a labelling arrow but this close the previous AC_layer.")\
        + _("\n\n  The GIMP grid or guide could be helpful to align many elements. N.B.: to")\
        + _("\nproduce a curve path 'click+drag' when placing an anchor or on the path after.")\
        + _("\n  <b>Warning:</b> keep initial image, don't remove 'AC_vectors' path or change arrow")\
        + _("\nor element layer (top under AC_group) while the plug-in is active.")
        self.label.set_label(prompt_line)
        self.next_flag = 'el_Y'    # identify next_elem

        # there was an actual arrow, part of one or label
        if self.arrow_done :
            # if change of anchor position from actual
            if self.is_virtual :
                self.update_Arrow()

            # for style with labelling use this to put a label inside the circle.
            if self.segment_asterix == '*' :
                self.index_state = 10
                if self.may_put_label() :
                    return  # put a label & next AC_arrow

            # merge layer, do not increase 'cr' (counter) yet
            if self.segment_cr > 1 : self.merge_elem()

            if self.choice_i == 2 :
                self.measurements.append((self.arrow_cr, self.segment_cr, self.l_arrow, self.theta))

            # Indicate element mode in the info line by a number > 1
            self.segment_cr += 1
            self.layer = gimp.Layer(self.img, _("AC_element"), self.img.width,\
              self.img.height, self.IMG_TYPE, 100, NORMAL_MODE)
            pdb.gimp_image_insert_layer(self.img, self.layer, self.Lgroup, 0)

            # message in 'Status'
            self.index_state = 12
            self.pre_arrow = [self.l_arrow, self.theta, self.choice_i, self.x1, self.y1]

            self.arrow_done = False
        else :
            # No previous arrow done on this layer, error message
            self.next_error()
        return

    def next_arrow_cb(self, data=None) :
        """
        Automate the layer creation for this plug-in, with action name & some
            basic explanations in tooltip.

        Callback from action button 'Next arrow'
        """

        if (not self.start_flag) : return
        # leave trace of last next action; about 75 chars per line?
        if self.index_state == 12 or not self.arrow_done :
            mess_block = _("<b>stocking blocked</b> by an empty")
        else : mess_block = _("stocked the previous active ")
        prompt_line = \
          _("  <b>Next arrow:</b> this was the last action clicked and ") + mess_block\
          + _("\nlayer. Before the drawing of the arrow, drag the anchors to the desired places.")\
          + _("\n\n  If you mistakenly create a new anchor, erase it with 'Back Space'.")\
          + _("\nTo have two anchors selected: 'Shift+click' on the one not selected (solid dot")\
          + _("\none) or click on the path; this permits a translation movement of the path when")\
          + _("\nyou drag one anchor. One exits this state by 'Shift+click' on an anchor.")
        self.label.set_label(prompt_line)
        self.next_flag = 'ar_Y'    # identify 'next_arrow_cb' proc

        # there was an actual arrow or part of, in active layer
        if self.arrow_done :
            # if change of anchor position from actual
            if self.is_virtual :
                self.update_Arrow()
            if self.choice_i == 2 :
                self.measurements.append((self.arrow_cr, self.segment_cr, \
                    self.l_arrow, self.theta))

            # if from 'Next element'
            if self.segment_cr > 1 :
                self.merge_elem()
                self.segment_cr = 1
            else :
                self.layer.attach_new_parasite('layer-info', 1, self.parasite_txt %
                    (self.l_arrow, self.theta, self.choice_i, self.x1, self.y1))
                    # tail position: self.x1, self.y1

            # create a new arrow layer
            self.arrow_cr += 1
            self.layer = gimp.Layer(self.img, _("AC_arrow #") + str(self.arrow_cr),\
                self.img.width, self.img.height, self.IMG_TYPE, 100, NORMAL_MODE)
            pdb.gimp_image_insert_layer(self.img, self.layer, self.Lgroup, 0)

            # recall self.pre_arrow info from layer parasite
            self.get_pre_layer_parasite()

            # message in 'Status'
            self.index_state = 12
            pdb.gimp_displays_flush()
            self.arrow_done = False
        else :
            # No previous arrow done, error message: self.index_state = 11
            self.next_error()
        return

    def press_close_cb(self, data=None) :
        """
        Callback (..._cb) from button 'Close'
        """

        if self.arrow_done :
            if self.choice_i == 2 :
                self.measurements.append((self.arrow_cr, self.segment_cr, self.l_arrow, self.theta))

            if self.segment_cr > 1 : self.merge_elem()
            else :
                self.layer.attach_new_parasite('layer-info', 1, self.parasite_txt\
                    % (self.l_arrow, self.theta, self.choice_i, self.x1, self.y1))

        # save label info in AC_group parasite 'label-info'
        if self.label_cr != self.style5_cr :    # changed from previous
            self.Lgroup.attach_new_parasite('label-info', 1, "%s, %s, %s, %f, %f, %d"\
              % (self.pre_char, self.chara, self.fontname, self.font_size, self.pre_quotient,
                 self.style5_cr))
            # next, for new label text, may interfere later with 'status' previous coord.
            if self.text_flag :
                pdb.gimp_image_resize_to_layers(self.img)

        # stop 'status' or 'anchors' and 'gtk.main' threads
        if self.source_anchors : source_remove(self.source_anchors)
        else :
            # save present arrow in image parasite 'prestyle-info'
            self.img.attach_new_parasite('prestyle-info', 1, "%s, %d, %f, %f, %f, %f"\
              % (self.text_flag, self.choice_i, self.sliders['wingSize'],
                 self.sliders['wingAngle'], self.sliders['brush'], self.sliders['#3']))
            # to save a AC_vectors to an image parasite 'AC_vectors-path'
            string = pdb.gimp_vectors_export_to_string(self.img, self.vectors_copy)
            self.img.attach_new_parasite('AC_vectors-path', 1, "%s" % string)

            source_remove(self.source_status)

        # return to upper layer level before quitting? or vectors non active?
        self.btnc.connect("released", gtk.main_quit)
        # measurements is my problem now, to have report in ArrowsCreator?
        return  # self.measurements