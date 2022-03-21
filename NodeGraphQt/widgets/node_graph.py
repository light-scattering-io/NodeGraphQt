from Qt import QtWidgets

from NodeGraphQt.constants import (
    NODE_SEL_BORDER_COLOR,
    VIEWER_BG_COLOR,
    VIEWER_GRID_COLOR
)
from NodeGraphQt.widgets.viewer_nav import NodeNavigationWidget


class NodeGraphWidget(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super(NodeGraphWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.setTabBarAutoHide(True)
        text_color = self.palette().text().color().toTuple()
        style_dict = {
            'QTabWidget::pane': {
                'background': 'rgb({0},{1},{2})'.format(*VIEWER_BG_COLOR),
                'border': '0px',
                'border-top': '1px solid rgb({0},{1},{2})'
                              .format(*VIEWER_BG_COLOR),
            },
            'QTabBar::tab': {
                'background': 'rgb({0},{1},{2})'.format(*VIEWER_BG_COLOR),
                'border': '0px solid black',
                'color': 'rgba({0},{1},{2},45)'.format(*text_color),
                'min-width': '10px',
                'padding': '8px 20px',
            },
            'QTabBar::tab:selected': {
                'color': 'rgb({0},{1},{2})'.format(*text_color),
                'background': 'rgb({0},{1},{2})'.format(*VIEWER_BG_COLOR),
                'margin-bottom': '-1px',
            },
            'QTabBar::tab:hover': {
                'color': 'rgb({0}, {1}, {2})'.format(*NODE_SEL_BORDER_COLOR),
                'background': 'rgb({0}, {1}, {2})'.format(*VIEWER_GRID_COLOR),
            }
        }
        stylesheet = ''
        for css_class, css in style_dict.items():
            style = '{} {{\n'.format(css_class)
            for elm_name, elm_val in css.items():
                style += '  {}:{};\n'.format(elm_name, elm_val)
            style += '}\n'
            stylesheet += style
        self.setStyleSheet(stylesheet)

    def add_viewer(self, viewer, name, node_id):
        self.addTab(viewer, name)
        index = self.indexOf(viewer)
        self.setTabToolTip(index, node_id)
        self.setCurrentIndex(index)

    def remove_viewer(self, viewer):
        index = self.indexOf(viewer)
        self.removeTab(index)


class SubGraphWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, graph=None):
        super(SubGraphWidget, self).__init__(parent)
        self._graph = graph
        self._navigator = NodeNavigationWidget()
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(1)
        self._layout.addWidget(self._navigator)

        self._viewer_widgets = {}
        self._viewer_current = None

    @property
    def navigator(self):
        return self._navigator

    def add_viewer(self, viewer, name, node_id):
        if viewer in self._viewer_widgets:
            return

        if self._viewer_current:
            self.hide_viewer(self._viewer_current)

        self._navigator.add_label_item(name, node_id)
        self._layout.addWidget(viewer)
        self._viewer_widgets[viewer] = node_id
        self._viewer_current = viewer
        self._viewer_current.show()

    def remove_viewer(self, viewer=None):
        if viewer is None and self._viewer_current:
            viewer = self._viewer_current
        node_id = self._viewer_widgets.pop(viewer)
        self._navigator.remove_label_item(node_id)
        self._layout.removeWidget(viewer)
        viewer.deleteLater()

    def hide_viewer(self, viewer):
        self._layout.removeWidget(viewer)
        viewer.hide()

    def show_viewer(self, viewer):
        if viewer == self._viewer_current:
            self._viewer_current.show()
            return
        if viewer in self._viewer_widgets:
            if self._viewer_current:
                self.hide_viewer(self._viewer_current)
            self._layout.addWidget(viewer)
            self._viewer_current = viewer
            self._viewer_current.show()
