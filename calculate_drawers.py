import itertools
 
tandem_kinds = [
    'TANDEM plus BLUMOTION',
    'TANDEM plus TIP-ON',
    'TANDEM plus',
    'TANDEM BLUMOTION',
    'TANDEM TIP-ON',
    'TANDEM',
]
tandem_lower_paddings = {
    'TANDEM plus BLUMOTION': 27.5,
    'TANDEM plus TIP-ON': 27.5,
    'TANDEM plus': 27.5,
    'TANDEM BLUMOTION': 24.5,
    'TANDEM TIP-ON': 22.5,
    'TANDEM': 22.5,
}
tandem_nominal_lengths = {
    'TANDEM plus BLUMOTION': [250, 270, 300, 350, 400, 450, 500, 550],
    'TANDEM plus TIP-ON': [250, 270, 300, 350, 400, 450, 500, 550],
    'TANDEM plus': [250, 270, 300, 350, 400, 450, 500, 550],
    'TANDEM BLUMOTION': [270, 300, 350, 400, 450, 500, 550],
    'TANDEM TIP-ON': [270, 300, 350, 400, 450, 500, 550],
    'TANDEM': [270, 300, 350, 400, 450, 500, 550],
}
tandem_upper_padding = 7
tip_on_wiggle_room = 4
drawer_side_extension_length = 10  # отступ от края до паза под полик в боковинах ящиков. взято от балды, нужно выяснить
drawer_thickness = 16


print('Виды TANDEM:')
for i, tandem_kind in enumerate(tandem_kinds):
	print(i, tandem_kind)
tandem_kind = tandem_kinds[int(input('Используемый вид (0-{}):'.format(len(tandem_kinds) - 1)))]
 
widths = [int(x) for x in input('ширины ящиков:').split()]
heights = [int(x) for x in input('высоты ящиков:').split()]
depth = int(input('глубина изделия:'))
facade_thickness = int(input('толщина фасада ящиков:'))
back_thickness = int(input('толщина задней стенки:'))
drawer_bottom_thickness = int(input('толщина полика ящиков:'))
carcass_thickness = int(input('толщина внутренних перегородок'))
inner = bool(input('вкладной ли фасад? (1/0):'))

stabiliser = posistop = False
if 'BLUMOTION' in tandem_kind:
	if inner:
		posistop = bool(input('есть ли упор по глубине? (1/0):'))
	else:
		stabiliser = bool(input('есть ли стабилизатор? (1/0):'))


parts = []

for width, height in itertools.product(widths, heights):
	lower_padding = tandem_lower_paddings[tandem_kind]
	nominal_lengths = tandem_nominal_lengths[tandem_kind]
	back_padding = 3

	if inner and 'TIP-ON' in tandem_kind:
		back_padding += 4
	
	if stabiliser:
		back_padding += 12

	if posistop:
		back_padding += 2

	if inner:
		max_nominal_length = depth - back_thickness - back_padding - facade_thickness
	else:
		max_nominal_length = depth - back_thickness - back_padding + tip_on_wiggle_room

	nominal_length = max(filter(lambda x: x < max_nominal_length, nominal_lengths))
	drawer_depth = nominal_length - 10
	drawer_width =  width - 10
	drawer_height = height - lower_padding - tandem_upper_padding  # это высота по полику, боковины больше

	drawer_parts = []
	drawer_parts.append((drawer_depth, drawer_width - drawer_thickness * 2 + 6 * 2))  # полик
	drawer_parts.extend([(drawer_width - drawer_thickness * 2, drawer_height - drawer_bottom_thickness)] * 2)  # поперечины
	drawer_parts.extend([(drawer_depth, drawer_height + drawer_side_extension_length)] * 2)  # боковины

	# TODO: фасад

	parts.extend(drawer_parts)

print(parts)