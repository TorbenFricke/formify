from formify.controls import *
from formify.layout import *
import formify, shapes
import copy

plot = ControlMatplotlib()
form = Form(
	Col(
		Row(
			ControlFloat(variable_name="x"),
			ControlFloat(variable_name="y"),
		),
		ControlText(variable_name="color", value="red"),
		ConditionalForm({
			"rectangle": Col(
				ControlFloat(variable_name="width"),
				ControlFloat(variable_name="height"),
				ControlFloat("Angle in °", variable_name="angle"),
			),
			"circle": Col(
				ControlFloat(variable_name="radius"),
			),
			"n_gon": Col(
				ControlInt(variable_name="corners"),
				ControlFloat(variable_name="radius"),
			),
			"star": Col(
				ControlInt(variable_name="corners"),
				ControlFloat(variable_name="inner_radius"),
				ControlFloat(variable_name="outer_radius"),
			),
		}, variable_name="__flatten__"),
	)
)

list_form = ListForm(
	form,
	display_name_callback=lambda x: f'{x["type"]} ({x["color"]})',
	variable_name="list_form"
)

def _draw():
	# setup
	plot.fig.clear()
	ax = plot.fig.subplots()
	ax.set_aspect('equal')

	# plotting
	for data in copy.deepcopy(list_form.value):
		func = getattr(shapes, data.pop("type"))
		func(ax, **data)

	# show
	ax.plot()
	plot.draw()

draw = formify.tools.BackgroundMethod(_draw, lazy=True)
form.change.subscribe(draw)

formify.MainWindow(
	Row(
		Segment(
			h2("Shapes"),
			list_form,
		),
		plot
	),
	margin=8
)