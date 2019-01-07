# -*- coding: utf-8 -*-

"""
Wraps leaflet Polyline, Polygon, Rectangle, Circlem and CircleMarker

"""

from __future__ import absolute_import, division, print_function

import json

from branca.element import CssLink, Element, Figure, JavascriptLink, MacroElement  # noqa

from folium.map import Marker

from jinja2 import Template


def path_options(line=False, radius=False, **kwargs):
    """
    Contains options and constants shared between vector overlays
    (Polygon, Polyline, Circle, CircleMarker, and Rectangle).

    Parameters
    ----------
    stroke: Bool, True
        Whether to draw stroke along the path.
        Set it to false to disable borders on polygons or circles.
    color: str, '#3388ff'
        Stroke color.
    weight: int, 3
        Stroke width in pixels.
    opacity: float, 1.0
        Stroke opacity.
    line_cap: str, 'round' (lineCap)
        A string that defines shape to be used at the end of the stroke.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linecap
    line_join: str, 'round' (lineJoin)
        A string that defines shape to be used at the corners of the stroke.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linejoin
    dash_array: str, None (dashArray)
        A string that defines the stroke dash pattern.
        Doesn't work on Canvas-powered layers in some old browsers.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dasharray
    dash_offset:, str, None (dashOffset)
        A string that defines the distance into the dash pattern to start the dash.
        Doesn't work on Canvas-powered layers in some old browsers.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dashoffset
    fill: Bool, False
        Whether to fill the path with color.
        Set it to false to disable filling on polygons or circles.
    fill_color: str, default to `color` (fillColor)
        Fill color. Defaults to the value of the color option.
    fill_opacity: float, 0.2 (fillOpacity)
        Fill opacity.
    fill_rule: str, 'evenodd' (fillRule)
        A string that defines how the inside of a shape is determined.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule
    bubbling_mouse_events: Bool, True (bubblingMouseEvents)
        When true a mouse event on this path will trigger the same event on the
        map (unless L.DomEvent.stopPropagation is used).

    Note that the presence of `fill_color` will override `fill=False`.

    See https://leafletjs.com/reference-1.4.0.html#path

    """

    extra_options = {}
    if line:
        extra_options = {
            'smoothFactor': kwargs.pop('smooth_factor', 1.0),
            'noClip': kwargs.pop('no_clip', False),
        }
    if radius:
        extra_options.update({'radius': radius})

    color = kwargs.pop('color', '#3388ff')
    fill_color = kwargs.pop('fill_color', False)
    if fill_color:
        fill = True
    elif not fill_color:
        fill_color = color
        fill = kwargs.pop('fill', False)

    default = {
        'stroke': kwargs.pop('stroke', True),
        'color': color,
        'weight': kwargs.pop('weight', 3),
        'opacity': kwargs.pop('opacity', 1.0),
        'lineCap': kwargs.pop('line_cap', 'round'),
        'lineJoin': kwargs.pop('line_join', 'round'),
        'dashArray': kwargs.pop('dash_array', None),
        'dashOffset': kwargs.pop('dash_offset', None),
        'fill': fill,
        'fillColor': fill_color,
        'fillOpacity': kwargs.pop('fill_opacity', 0.2),
        'fillRule': kwargs.pop('fill_rule', 'evenodd'),
        'bubblingMouseEvents': kwargs.pop('bubbling_mouse_events', True),
    }
    default.update(extra_options)
    return default


def _parse_options(line=False, radius=False, **kwargs):
    options = path_options(line=line, radius=radius, **kwargs)
    return json.dumps(options, sort_keys=True, indent=2)


class PolyLine(Marker):
    """
    Class for drawing polyline overlays on a map.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: str or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.
    smooth_factor: float, default 1.0
        How much to simplify the polyline on each zoom level.
        More means better performance and smoother look,
        and less means more accurate representation.
    no_clip: Bool, default False
        Disable polyline clipping.


    See https://leafletjs.com/reference-1.4.0.html#polyline

    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.polyline(
                    {{this.location}},
                    {{ this.options }}
                    )
                    .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)  # noqa

    def __init__(self, locations, popup=None, tooltip=None, **kwargs):
        super(PolyLine, self).__init__(location=locations, popup=popup,
                                       tooltip=tooltip)
        self._name = 'PolyLine'
        self.options = _parse_options(line=True, **kwargs)


class Polygon(Marker):
    """
    Class for drawing polygon overlays on a map.

    Extends :func:`folium.vector_layers.PolyLine`.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: string or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.


    See https://leafletjs.com/reference-1.4.0.html#polygon

    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{this.get_name()}} = L.polygon(
                {{this.location}},
                {{ this.options }}
                )
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def __init__(self, locations, popup=None, tooltip=None, **kwargs):
        super(Polygon, self).__init__(locations, popup=popup, tooltip=tooltip)
        self._name = 'Polygon'
        self.options = _parse_options(line=True, **kwargs)


class Envelope_Polygon_from_Points(Marker):
    """
    Class for drawing polygon overlays that envelope a given list of points on a map.

    Extends :func:`folium.vector_layers.Polygon`.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: string or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.

    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{this.get_name()}} = L.polygon(
                {{this.location}},
                {{ this.options }}
                )
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def __init__(self, locations, popup=None, tooltip=None, **kwargs):
        
        #The location list has to contain at least 2 points
        if len(locations) > 1 and not locations == None:
        
            from operator import itemgetter
        
            Points = sorted(locations,key=itemgetter(0))
            X_Min = Points[0]
            X_Max = Points[len(Points)-1]
        
            Points = sorted(Points,key=itemgetter(1))
            Y_Min = Points[0]
            Y_Max = Points[len(Points)-1]
        
            Upper_Left = (X_Min[0], Y_Max[1])
            Upper_Right = (X_Max[0], Y_Max[1])
            Lower_Right = (X_Max[0], Y_Min[1])
            Lower_Left = (X_Min[0], Y_Min[1])
        
            locations = [Upper_Left, Upper_Right, Lower_Right, Lower_Left]

        super(Envelope_Polygon_from_Points, self).__init__(locations, popup=popup, tooltip=tooltip)
        self._name = 'Envelope_Polygon_from_Points'
        self.options = _parse_options(line=True, **kwargs)


class ConvexHull_Polygon_from_Points(Marker):
    """
    Class for drawing polygon overlays that ensemble a ConvexHull around a given list of points on a map.

    Extends :func:`folium.vector_layers.Polygon`.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: string or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.

    Based on https://stackoverflow.com/questions/39996028/draw-a-closed-and-filled-contour, accessed: 29.12.2018
    
    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{this.get_name()}} = L.polygon(
                {{this.location}},
                {{ this.options }}
                )
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def __init__(self, locations, popup=None, tooltip=None, **kwargs):
        
        #The location list has to contain at least 3 points
        if len(locations) > 2 and not locations == None:
            from scipy.spatial import ConvexHull
            locations = [locations[i] for i in ConvexHull(locations).vertices]

        super(ConvexHull_Polygon_from_Points, self).__init__(locations, popup=popup, tooltip=tooltip)
        self._name = 'ConvexHull_Polygon_from_Points'
        self.options = _parse_options(line=True, **kwargs)


class Rectangle(Marker):
    """
    Class for drawing rectangle overlays on a map.

    Extends :func:`folium.vector_layers.Polygon`.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: string or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.


    See https://leafletjs.com/reference-1.4.0.html#rectangle

    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{this.get_name()}} = L.rectangle(
                {{this.location}},
                {{ this.options }}
                )
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def __init__(self, bounds, popup=None, tooltip=None, **kwargs):
        super(Rectangle, self).__init__(location=bounds, popup=popup,
                                        tooltip=tooltip)
        self._name = 'rectangle'
        self.options = _parse_options(line=True, **kwargs)


class Circle(Marker):
    """
    Class for drawing circle overlays on a map.

    It's an approximation and starts to diverge from a real circle closer to poles
    (due to projection distortion).

    Extends :func:`folium.vector_layers.CircleMarker`.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: string or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.
    radius: float
        Radius of the circle, in meters.


    See https://leafletjs.com/reference-1.4.0.html#circle

    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{this.get_name()}} = L.circle(
                [{{this.location[0]}}, {{this.location[1]}}],
                {{ this.options }}
                )
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def __init__(self, location, radius, popup=None, tooltip=None, **kwargs):
        super(Circle, self).__init__(location=location, popup=popup,
                                     tooltip=tooltip)
        self._name = 'circle'
        self.options = _parse_options(line=False, radius=radius, **kwargs)


class CircleMarker(Marker):
    """
    A circle of a fixed size with radius specified in pixels.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: string or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.
    radius: float, default 10
        Radius of the circle marker, in pixels.


    See https://leafletjs.com/reference-1.4.0.html#circlemarker

    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.circleMarker(
                [{{this.location[0]}}, {{this.location[1]}}],
                {{ this.options }}
                )
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def __init__(self, location, radius=10, popup=None, tooltip=None, **kwargs):
        super(CircleMarker, self).__init__(location=location, popup=popup,
                                           tooltip=tooltip)
        self._name = 'CircleMarker'
        self.options = _parse_options(line=False, radius=radius, **kwargs)
