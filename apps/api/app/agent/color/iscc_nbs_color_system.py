from app.agent.models import ColorRange

# Dictionary of ISCC-NBS color categories with representative hex values
ISCC_NBS_COLORS = {
  'Vivid Pink': '#FFB5BA',
  'Strong Pink': '#EA9399',
  'Deep Pink': '#E4717A',
  'Light Pink': '#F9CCCA',
  'Moderate Pink': '#DEA5A4',
  'Dark Pink': '#C08081',
  'Pale Pink': '#EAD8D7',
  'Grayish Pink': '#C4AEAD',
  'Pinkish White': '#EAE3E1',
  'Pinkish Gray': '#C1B6B3',
  'Vivid Red': '#BE0032',
  'Strong Red': '#BC3F4A',
  'Deep Red': '#841B2D',
  'Very Deep Red': '#5C0923',
  'Moderate Red': '#AB4E52',
  'Dark Red': '#722F37',
  'Very Dark Red': '#3F1728',
  'Light Grayish Red': '#AD8884',
  'Grayish Red': '#905D5D',
  'Dark Grayish Red': '#543D3F',
  'Blackish Red': '#2E1D21',
  'Reddish Gray': '#8F817F',
  'Dark Reddish Gray': '#5C504F',
  'Reddish Black': '#282022',
  'Vivid Yellowish Pink': '#FFB7A5',
  'Strong Yellowish Pink': '#F99379',
  'Deep Yellowish Pink': '#E66721', # closest is Coral Orange (228, 105, 76)
  'Light Yellowish Pink': '#F4C2C2',
  'Moderate Yellowish Pink': '#D9A6A9',
  'Dark Yellowish Pink': '#C48379',
  'Pale Yellowish Pink': '#ECD5C5',
  'Grayish Yellowish Pink': '#C7ADA3',
  'Brownish Pink': '#C2AC99',
  'Vivid Reddish Orange': '#E25822',
  'Strong Reddish Orange': '#D9603B',
  'Deep Reddish Orange': '#AA381E',
  'Moderate Reddish Orange': '#CB6D51',
  'Dark Reddish Orange': '#9E4732',
  'Grayish Reddish Orange': '#B4745E',
  'Strong Reddish Brown': '#882D17',
  'Deep Reddish Brown': '#56070C',
  'Light Reddish Brown': '#A87C6D',
  'Moderate Reddish Brown': '#79443B',
  'Dark Reddish Brown': '#3E1D1E',
  'Light Grayish Reddish Brown': '#977F73',
  'Grayish Reddish Brown': '#674C47',
  'Dark Grayish Reddish Brown': '#43302E',
  'Vivid Orange': '#F38400',
  'Brilliant Orange': '#FD943F',
  'Strong Orange': '#ED872D',
  'Deep Orange': '#BE6516',
  'Light Orange': '#FAB57F',
  'Moderate Orange': '#D99058',
  'Brownish Orange': '#AE6938',
  'Strong Brown': '#80461B',
  'Deep Brown': '#593319',
  'Light Brown': '#A67B5B',
  'Moderate Brown': '#6F4E37',
  'Dark Brown': '#422518',
  'Light Grayish Brown': '#958070',
  'Grayish Brown': '#635147',
  'Dark Grayish Brown': '#3E322C',
  'Light Brownish Gray': '#8E8279',
  'Brownish Gray': '#5B504F',
  'Brownish Black': '#28201C',
  'Vivid Orange Yellow': '#F6A600',
  'Brilliant Orange Yellow': '#FFC14F',
  'Strong Orange Yellow': '#EAA221',
  'Deep Orange Yellow': '#C98500',
  'Light Orange Yellow': '#FBC97F',
  'Moderate Orange Yellow': '#E3A857',
  'Dark Orange Yellow': '#BE8A3D',
  'Pale Orange Yellow': '#FAD6A5',
  'Strong Yellowish Brown': '#996515',
  'Deep Yellowish Brown': '#654522',
  'Light Yellowish Brown': '#C19A6B',
  'Moderate Yellowish Brown': '#826644',
  'Dark Yellowish Brown': '#4B3621',
  'Light Grayish Yellowish Brown': '#AE9B82',
  'Grayish Yellowish Brown': '#7E6D5A',
  'Dark Grayish Yellowish Brown': '#483C32',
  'Vivid Yellow': '#F3C300',
  'Brilliant Yellow': '#FADA5E',
  'Strong Yellow': '#D4AF37',
  'Deep Yellow': '#AF8D13',
  'Light Yellow': '#F8DE7E',
  'Moderate Yellow': '#C9AE5D',
  'Dark Yellow': '#AB9144',
  'Pale Yellow': '#F3E5AB',
  'Grayish Yellow': '#C2B280',
  'Dark Grayish Yellow': '#A18F60',
  'Yellowish White': '#F0EAD6',
  'Yellowish Gray': '#BFB8A5',
  'Light Olive Brown': '#967117',
  'Moderate Olive Brown': '#6C541E',
  'Dark Olive Brown': '#3B3121',
  'Vivid Greenish Yellow': '#DCD300',
  'Brilliant Greenish Yellow': '#E9E450',
  'Strong Greenish Yellow': '#BEB72E',
  'Deep Greenish Yellow': '#9B9400',
  'Light Greenish Yellow': '#EAE679',
  'Moderate Greenish Yellow': '#B9B459',
  'Dark Greenish Yellow': '#98943E',
  'Pale Greenish Yellow': '#EBE8A4',
  'Grayish Greenish Yellow': '#B9B57D',
  'Light Olive': '#867E36',
  'Moderate Olive': '#665D1E',
  'Dark Olive': '#403D21',
  'Light Grayish Olive': '#8C8767',
  'Grayish Olive': '#5B5842',
  'Dark Grayish Olive': '#363527',
  'Light Olive Gray': '#8A8776',
  'Olive Gray': '#57554C',
  'Olive Black': '#25241D',
  'Vivid Yellow Green': '#8DB600',
  'Brilliant Yellow Green': '#BDDA57',
  'Strong Yellow Green': '#7E9F2E',
  'Deep Yellow Green': '#467129',
  'Light Yellow Green': '#C9DC89',
  'Moderate Yellow Green': '#8A9A5B',
  'Pale Yellow Green': '#DADFB7',
  'Grayish Yellow Green': '#8F9779',
  'Strong Olive Green': '#404F00',
  'Deep Olive Green': '#232F00',
  'Moderate Olive Green': '#4A5D23',
  'Dark Olive Green': '#2B3D26',
  'Grayish Olive Green': '#515744',
  'Dark Grayish Olive Green': '#31362B',
  'Vivid Yellowish Green': '#27A64C',
  'Brilliant Yellowish Green': '#83D37D',
  'Strong Yellowish Green': '#44944A',
  'Deep Yellowish Green': '#00622D',
  'Very Deep Yellowish Green': '#003118',
  'Very Light Yellowish Green': '#B6E5AF',
  'Light Yellowish Green': '#93C592',
  'Moderate Yellowish Green': '#679267',
  'Dark Yellowish Green': '#355E3B',
  'Very Dark Yellowish Green': '#173620',
  'Vivid Green': '#008856',
  'Brilliant Green': '#3EB489',
  'Strong Green': '#007959',
  'Deep Green': '#00543D',
  'Very Light Green': '#8ED1B2',
  'Light Green': '#6AAB8E',
  'Moderate Green': '#3B7861',
  'Dark Green': '#1B4D3E',
  'Very Dark Green': '#1C352D',
  'Very Pale Green': '#C7E6D7',
  'Pale Green': '#8DA399',
  'Grayish Green': '#5E716A',
  'Dark Grayish Green': '#3A4B47',
  'Blackish Green': '#1A2421',
  'Greenish White': '#DFEDE8',
  'Light Greenish Gray': '#B2BEB5',
  'Greenish Gray': '#7D8984',
  'Dark Greenish Gray': '#4E5755',
  'Greenish Black': '#1E2321',
  'Vivid Bluish Green': '#008882',
  'Brilliant Bluish Green': '#00A693',
  'Strong Bluish Green': '#007A74',
  'Deep Bluish Green': '#00443F',
  'Very Light Bluish Green': '#96DED1',
  'Light Bluish Green': '#66ADA4',
  'Moderate Bluish Green': '#317873',
  'Dark Bluish Green': '#004B49',
  'Very Dark Bluish Green': '#002A29',
  'Vivid Greenish Blue': '#0085A1',
  'Brilliant Greenish Blue': '#239EBA',
  'Strong Greenish Blue': '#007791',
  'Deep Greenish Blue': '#2E8495',
  'Very Light Greenish Blue': '#9CD1DC',
  'Light Greenish Blue': '#66AABC',
  'Moderate Greenish Blue': '#367588',
  'Dark Greenish Blue': '#004958',
  'Very Dark Greenish Blue': '#002E3B',
  'Vivid Blue': '#00A1C2',
  'Brilliant Blue': '#4997D0',
  'Strong Blue': '#0067A5',
  'Deep Blue': '#00416A',
  'Very Light Blue': '#A1CAF1',
  'Light Blue': '#70A3CC',
  'Moderate Blue': '#436B95',
  'Dark Blue': '#00304E',
  'Very Pale Blue': '#BCD4E6',
  'Pale Blue': '#91A3B0',
  'Grayish Blue': '#536878',
  'Dark Grayish Blue': '#36454F',
  'Blackish Blue': '#202830',
  'Bluish White': '#E9E9ED',
  'Light Bluish Gray': '#B4BCC0',
  'Bluish Gray': '#81878B',
  'Dark Bluish Gray': '#51585E',
  'Bluish Black': '#202428',
  'Vivid Purplish Blue': '#30267A',
  'Brilliant Purplish Blue': '#6C79B8',
  'Strong Purplish Blue': '#545AA7',
  'Deep Purplish Blue': '#272458',
  'Very Light Purplish Blue': '#B3BCE2',
  'Light Purplish Blue': '#8791BF',
  'Moderate Purplish Blue': '#4E5180',
  'Dark Purplish Blue': '#252440',
  'Very Pale Purplish Blue': '#C0C8E1',
  'Pale Purplish Blue': '#8C92AC',
  'Grayish Purplish Blue': '#4C516D',
  'Vivid Violet': '#9065CA',
  'Brilliant Violet': '#7E73B8',
  'Strong Violet': '#604E97',
  'Deep Violet': '#32174D',
  'Very Light Violet': '#DCD0FF',
  'Light Violet': '#8C82B6',
  'Moderate Violet': '#604E81',
  'Dark Violet': '#2F2140',
  'Very Pale Violet': '#C4C3DD',
  'Pale Violet': '#9690AB',
  'Grayish Violet': '#554C69',
  'Vivid Purple': '#9A4EAE',
  'Brilliant Purple': '#D399E6',
  'Strong Purple': '#875692',
  'Deep Purple': '#602F6B',
  'Very Deep Purple': '#401A4C',
  'Very Light Purple': '#D5BADB',
  'Light Purple': '#B695C0',
  'Moderate Purple': '#86608E',
  'Dark Purple': '#563C5C',
  'Very Dark Purple': '#301934',
  'Very Pale Purple': '#D6CADD',
  'Pale Purple': '#AA98A9',
  'Grayish Purple': '#796878',
  'Dark Grayish Purple': '#50404D',
  'Blackish Purple': '#291E29',
  'Purplish White': '#E8E3E5',
  'Light Purplish Gray': '#BFB9BD',
  'Purplish Gray': '#8B8589',
  'Dark Purplish Gray': '#5D555B',
  'Purplish Black': '#242124',
  'Vivid Reddish Purple': '#870074',
  'Strong Reddish Purple': '#9E4F88',
  'Deep Reddish Purple': '#702963',
  'Very Deep Reddish Purple': '#54194E',
  'Light Reddish Purple': '#B784A7',
  'Moderate Reddish Purple': '#915C83',
  'Dark Reddish Purple': '#5D3954',
  'Very Dark Reddish Purple': '#341731',
  'Pale Reddish Purple': '#AA8A9E',
  'Grayish Reddish Purple': '#836479',
  'Brilliant Purplish Pink': '#FFC8D6',
  'Strong Purplish Pink': '#E68FAC',
  'Deep Purplish Pink': '#DE6FA1',
  'Light Purplish Pink': '#EFBBCC',
  'Moderate Purplish Pink': '#D597AE',
  'Dark Purplish Pink': '#C17E91',
  'Pale Purplish Pink': '#E8CCD7',
  'Grayish Purplish Pink': '#C3A6B1',
  'Vivid Purplish Red': '#CE4676',
  'Strong Purplish Red': '#B3446C',
  'Deep Purplish Red': '#78184A',
  'Very Deep Purplish Red': '#54133B',
  'Moderate Purplish Red': '#A8516E',
  'Dark Purplish Red': '#673147',
  'Very Dark Purplish Red': '#38152C',
  'Light Grayish Purplish Red': '#AF868E',
  'Grayish Purplish Red': '#915F6D',
  'White': '#F2F3F4',
  'Light Gray': '#B9B8B5',
  'Medium Gray': '#848482',
  'Dark Gray': '#555555',
  'Black': '#111111', # Darker than official ISCC black (#222222) because "Greenish Black" is darker than it
}

"""
Map of category names from the IBCC NBS color system mapped to Color Agent color categories
(`color_range`) and an analogous list of color names that are either secondary color category
names or common associated color names.

Some color categories used in IBCC NBS are also applied to the `analogous` colors list, because
they are not used in Color Agent's color categories or that any colors falling under them have
been generalized to fall under another category (e.g., "Violet" falls under "Purple").

See https://en.wikipedia.org/wiki/ISCC–NBS_system#Color_categories
"""
IBCC_NBS_CATEGORIES = {
    'Vivid Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Strong Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Deep Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Coral'],
    },
    'Light Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Moderate Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Dark Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Pale Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Grayish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Pinkish White': {
        'color_range': [ColorRange.Pink, ColorRange.White],
        'analogous': ['Blush'],
    },
    'Pinkish Gray': {
        'color_range': [ColorRange.Pink, ColorRange.Grey],
        'analogous': [],
    },
    'Vivid Red': {
        'color_range': [ColorRange.Red],
        'analogous': ['Fire Engine Red'],
    },
    'Strong Red': {
        'color_range': [ColorRange.Red],
        'analogous': ['Amaranth', 'Maroon', 'Vermillion'],
    },
    'Deep Red': {
        'color_range': [ColorRange.Red],
        'analogous': ['Cardinal', 'Crimson'],
    },
    'Very Deep Red': {
        'color_range': [ColorRange.Red],
        'analogous': ['Blood Red', 'Maroon'],
    },
    'Moderate Red': {
        'color_range': [ColorRange.Red],
        'analogous': [],
    },
    'Dark Red': {
        'color_range': [ColorRange.Red],
        'analogous': ['Burgundy'],
    },
    'Very Dark Red': {
        'color_range': [ColorRange.Brown, ColorRange.Red],
        'analogous': ['Barn Red'],
    },
    'Light Grayish Red': {
        'color_range': [ColorRange.Red],
        'analogous': [],
    },
    'Grayish Red': {
        'color_range': [ColorRange.Brown, ColorRange.Red],
        'analogous': ['Indian Red', 'Rose Taupe'],
    },
    'Dark Grayish Red': {
        'color_range': [ColorRange.Brown, ColorRange.Red],
        'analogous': [],
    },
    'Blackish Red': {
        'color_range': [ColorRange.Brown, ColorRange.Red],
        'analogous': [],
    },
    'Reddish Gray': {
        'color_range': [ColorRange.Red, ColorRange.Grey],
        'analogous': ['Taupe'],
    },
    'Dark Reddish Gray': {
        'color_range': [ColorRange.Red, ColorRange.Grey],
        'analogous': [],
    },
    'Reddish Black': {
        'color_range': [ColorRange.Black, ColorRange.Grey],
        'analogous': [],
    },
    'Vivid Yellowish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Coral', 'Salmon'],
    },
    'Strong Yellowish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Coral'],
    },
    'Deep Yellowish Pink': {
        'color_range': [ColorRange.Pink, ColorRange.Red],
        'analogous': ['Coral'],
    },
    'Light Yellowish Pink': {
        'color_range': [ ColorRange.Pink],
        'analogous': [],
    },
    'Moderate Yellowish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Cantaloupe'],
    },
    'Dark Yellowish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Pale Yellowish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Grayish Yellowish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Silver Pink'],
    },
    'Brownish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Vivid Reddish Orange': {
        'color_range': [ColorRange.Orange, ColorRange.Red],
        'analogous': ['Orangered', 'Scarlet', 'Tomato', 'Vermillion'],
    },
    'Strong Reddish Orange': {
        'color_range': [ColorRange.Orange, ColorRange.Red],
        'analogous': ['Salmon'],
    },
    'Deep Reddish Orange': {
        'color_range': [ColorRange.Brown, ColorRange.Orange, ColorRange.Red],
        'analogous': [],
    },
    'Moderate Reddish Orange': {
        'color_range': [ColorRange.Orange],
        'analogous': [],
    },
    'Dark Reddish Orange': {
        'color_range': [ColorRange.Brown, ColorRange.Orange],
        'analogous': ['Redwood'],
    },
    'Grayish Reddish Orange': {
        'color_range': [ColorRange.Orange],
        'analogous': [],
    },
    'Strong Reddish Brown': {
        'color_range': [ColorRange.Brown, ColorRange.Red],
        'analogous': [],
    },
    'Deep Reddish Brown': {
        'color_range': [ColorRange.Brown, ColorRange.Red],
        'analogous': ['Barn Red', 'Blood Red', 'Garnet', 'Maroon'],
    },
    'Light Reddish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Moderate Reddish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Dark Reddish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Light Grayish Reddish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Grayish Reddish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Dark Grayish Reddish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Vivid Orange': {
        'color_range': [ColorRange.Orange],
        'analogous': [],
    },
    'Brilliant Orange': {
        'color_range': [ColorRange.Orange],
        'analogous': [],
    },
    'Strong Orange': {
        'color_range': [ColorRange.Orange],
        'analogous': [],
    },
    'Deep Orange': {
        'color_range': [ColorRange.Brown, ColorRange.Orange],
        'analogous': [],
    },
    'Light Orange': {
        'color_range': [ColorRange.Orange],
        'analogous': [],
    },
    'Moderate Orange': {
        'color_range': [ColorRange.Orange],
        'analogous': [],
    },
    'Brownish Orange': {
        'color_range': [ColorRange.Brown, ColorRange.Orange],
        'analogous': [],
    },
    'Strong Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Deep Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Light Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Moderate Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Dark Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Light Grayish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Grayish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Dark Grayish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Light Brownish Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Brownish Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Brownish Black': {
        'color_range': [ColorRange.Black, ColorRange.Grey],
        'analogous': [],
    },
    'Vivid Orange Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': [],
    },
    'Brilliant Orange Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': ['Goldenrod'],
    },
    'Strong Orange Yellow': {
        'color_range': [ColorRange.Orange, ColorRange.Yellow],
        'analogous': ['Goldenrod'],
    },
    'Deep Orange Yellow': {
        'color_range': [ColorRange.Orange, ColorRange.Yellow],
        'analogous': [],
    },
    'Light Orange Yellow': {
        'color_range': [ColorRange.Orange, ColorRange.Yellow],
        'analogous': [],
    },
    'Moderate Orange Yellow': {
        'color_range': [ColorRange.Orange, ColorRange.Yellow],
        'analogous': [],
    },
    'Dark Orange Yellow': {
        'color_range': [ColorRange.Orange, ColorRange.Yellow],
        'analogous': [],
    },
    'Pale Orange Yellow': {
        'color_range': [ColorRange.Orange, ColorRange.Yellow],
        'analogous': [],
    },
    'Strong Yellowish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Deep Yellowish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Light Yellowish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Moderate Yellowish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Dark Yellowish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Light Grayish Yellowish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Grayish Yellowish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Dark Grayish Yellowish Brown': {
        'color_range': [ColorRange.Brown],
        'analogous': [],
    },
    'Vivid Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': [],
    },
    'Brilliant Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': [],
    },
    'Strong Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': ['Ochre'],
    },
    'Deep Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': ['Ochre'],
    },
    'Light Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': [],
    },
    'Moderate Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': [],
    },
    'Dark Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': [],
    },
    'Pale Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': ['Bone', 'Parchment'],
    },
    'Grayish Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': ['Bone', 'Parchment'],
    },
    'Dark Grayish Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': ['Bone'],
    },
    'Yellowish White': {
        'color_range': [ColorRange.White],
        'analogous': ['Bone', 'Champagne', 'Cream', 'Ivory'],
    },
    'Yellowish Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': ['Bone'],
    },
    'Light Olive Brown': {
        'color_range': [ColorRange.Brown, ColorRange.Olive],
        'analogous': [],
    },
    'Moderate Olive Brown': {
        'color_range': [ColorRange.Brown, ColorRange.Olive],
        'analogous': ['Golden Brown'],
    },
    'Dark Olive Brown': {
        'color_range': [ColorRange.Brown, ColorRange.Olive],
        'analogous': [],
    },
    'Vivid Greenish Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': [],
    },
    'Brilliant Greenish Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': [],
    },
    'Strong Greenish Yellow': {
        'color_range': [ColorRange.Green, ColorRange.Yellow],
        'analogous': [],
    },
    'Deep Greenish Yellow': {
        'color_range': [ColorRange.Green, ColorRange.Yellow],
        'analogous': [],
    },
    'Light Greenish Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': ['Bone'],
    },
    'Moderate Greenish Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': ['Bone', 'Khaki'],
    },
    'Dark Greenish Yellow': {
        'color_range': [ColorRange.Green, ColorRange.Yellow],
        'analogous': ['Khaki'],
    },
    'Pale Greenish Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': ['Bone'],
    },
    'Grayish Greenish Yellow': {
        'color_range': [ColorRange.Yellow],
        'analogous': ['Bone'],
    },
    'Light Olive': {
        'color_range': [ColorRange.Olive],
        'analogous': [],
    },
    'Moderate Olive': {
        'color_range': [ColorRange.Olive],
        'analogous': ['Green Gold'],
    },
    'Dark Olive': {
        'color_range': [ColorRange.Olive],
        'analogous': [],
    },
    'Light Grayish Olive': {
        'color_range': [ColorRange.Olive],
        'analogous': [],
    },
    'Grayish Olive': {
        'color_range': [ColorRange.Olive],
        'analogous': [],
    },
    'Dark Grayish Olive': {
        'color_range': [ColorRange.Olive],
        'analogous': [],
    },
    'Light Olive Gray': {
        'color_range': [ColorRange.Grey, ColorRange.Olive],
        'analogous': [],
    },
    'Olive Gray': {
        'color_range': [ColorRange.Grey, ColorRange.Olive],
        'analogous': [],
    },
    'Olive Black': {
        'color_range': [ColorRange.Black, ColorRange.Grey],
        'analogous': ['Charcoal'],
    },
    'Vivid Yellow Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Yellow Green'],
    },
    'Brilliant Yellow Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Yellow Green'],
    },
    'Strong Yellow Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Yellow Green'],
    },
    'Deep Yellow Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Yellow Green'],
    },
    'Light Yellow Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Yellow Green'],
    },
    'Moderate Yellow Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Yellow Green'],
    },
    'Pale Yellow Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Yellow Green'],
    },
    'Grayish Yellow Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Yellow Green'],
    },
    'Strong Olive Green': {
        'color_range': [ColorRange.Green, ColorRange.Olive],
        'analogous': [],
    },
    'Deep Olive Green': {
        'color_range': [ColorRange.Green, ColorRange.Olive],
        'analogous': [],
    },
    'Moderate Olive Green': {
        'color_range': [ColorRange.Green, ColorRange.Olive],
        'analogous': [],
    },
    'Dark Olive Green': {
        'color_range': [ColorRange.Green, ColorRange.Olive],
        'analogous': [],
    },
    'Grayish Olive Green': {
        'color_range': [ColorRange.Green, ColorRange.Olive],
        'analogous': [],
    },
    'Dark Grayish Olive Green': {
        'color_range': [ColorRange.Green, ColorRange.Olive],
        'analogous': [],
    },
    'Vivid Yellowish Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Yellow Green'],
    },
    'Brilliant Yellowish Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Lime'],
    },
    'Strong Yellowish Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Deep Yellowish Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Very Deep Yellowish Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Very Light Yellowish Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Mint'],
    },
    'Light Yellowish Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Mint'],
    },
    'Moderate Yellowish Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Mint'],
    },
    'Dark Yellowish Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Mint'],
    },
    'Very Dark Yellowish Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Vivid Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Emerald'],
    },
    'Brilliant Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Leaf Green'],
    },
    'Strong Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Deep Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Very Light Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Light Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Moderate Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Dark Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Very Dark Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Very Pale Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Pale Green': {
        'color_range': [ColorRange.Green],
        'analogous': [],
    },
    'Grayish Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Pine'],
    },
    'Dark Grayish Green': {
        'color_range': [ColorRange.Green],
        'analogous': ['Evergreen'],
    },
    'Blackish Green': {
        'color_range': [ColorRange.Green, ColorRange.Black],
        'analogous': [],
    },
    'Greenish White': {
        'color_range': [ColorRange.Green, ColorRange.Grey, ColorRange.White],
        'analogous': [],
    },
    'Light Greenish Gray': {
        'color_range': [ColorRange.Green, ColorRange.Grey],
        'analogous': [],
    },
    'Greenish Gray': {
        'color_range': [ColorRange.Green, ColorRange.Grey],
        'analogous': [],
    },
    'Dark Greenish Gray': {
        'color_range': [ColorRange.Green, ColorRange.Grey],
        'analogous': [],
    },
    'Greenish Black': {
        'color_range': [ColorRange.Black, ColorRange.Grey],
        'analogous': ['Onyx'],
    },
    'Vivid Bluish Green': {
        'color_range': [ColorRange.Green, ColorRange.Turquoise],
        'analogous': ['Teal'],
    },
    'Brilliant Bluish Green': {
        'color_range': [ColorRange.Green, ColorRange.Turquoise],
        'analogous': ['Teal'],
    },
    'Strong Bluish Green': {
        'color_range': [ColorRange.Green, ColorRange.Turquoise],
        'analogous': ['Teal'],
    },
    'Deep Bluish Green': {
        'color_range': [ColorRange.Green, ColorRange.Turquoise],
        'analogous': ['Teal'],
    },
    'Very Light Bluish Green': {
        'color_range': [ColorRange.Green, ColorRange.Turquoise],
        'analogous': ['Aqua', 'Teal'],
    },
    'Light Bluish Green': {
        'color_range': [ColorRange.Green, ColorRange.Turquoise],
        'analogous': ['Aqua', 'Teal'],
    },
    'Moderate Bluish Green': {
        'color_range': [ColorRange.Green, ColorRange.Turquoise],
        'analogous': ['Teal'],
    },
    'Dark Bluish Green': {
        'color_range': [ColorRange.Green, ColorRange.Turquoise],
        'analogous': ['Teal'],
    },
    'Very Dark Bluish Green': {
        'color_range': [ColorRange.Green, ColorRange.Turquoise],
        'analogous': ['Teal'],
    },
    'Vivid Greenish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Turquoise],
        'analogous': ['Cerulean', 'Cyan'],
    },
    'Brilliant Greenish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Turquoise],
        'analogous': ['Cyan'],
    },
    'Strong Greenish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Turquoise],
        'analogous': ['Cerulean', 'Cyan'],
    },
    'Deep Greenish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Turquoise],
        'analogous': ['Cerulean Blue', 'Cyan'],
    },
    'Very Light Greenish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Turquoise],
        'analogous': ['Cyan'],
    },
    'Light Greenish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Turquoise],
        'analogous': ['Cyan'],
    },
    'Moderate Greenish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Turquoise],
        'analogous': ['Cyan'],
    },
    'Dark Greenish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Turquoise],
        'analogous': ['Cyan'],
    },
    'Very Dark Greenish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Turquoise],
        'analogous': ['Cyan'],
    },
    'Vivid Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Azure', 'Celtic Blue', 'Midnight', 'Navy Blue', 'Ultramarine'],
    },
    'Brilliant Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Cornflower Blue'],
    },
    'Strong Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Azure'],
    },
    'Deep Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Azure', 'Royal Blue', 'Sapphire'],
    },
    'Very Light Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': [],
    },
    'Light Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Celestial Blue'],
    },
    'Moderate Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Steel Blue'],
    },
    'Dark Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Cool Black', 'Navy Blue', 'Space Cadet'],
    },
    'Very Pale Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Grey],
        'analogous': [],
    },
    'Pale Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Grey],
        'analogous': [],
    },
    'Grayish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Grey],
        'analogous': [],
    },
    'Dark Grayish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Grey],
        'analogous': [],
    },
    'Blackish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Black, ColorRange.Grey],
        'analogous': ['Midnight'],
    },
    'Bluish White': {
        'color_range': [ColorRange.Grey, ColorRange.White],
        'analogous': [],
    },
    'Light Bluish Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Bluish Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Dark Bluish Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Bluish Black': {
        'color_range': [ColorRange.Black, ColorRange.Grey],
        'analogous': [],
    },
    'Vivid Purplish Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Neon Blue'],
    },
    'Brilliant Purplish Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': [],
    },
    'Strong Purplish Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Ultramarine'],
    },
    'Deep Purplish Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': [],
    },
    'Very Light Purplish Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Periwinkle'],
    },
    'Light Purplish Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': [],
    },
    'Moderate Purplish Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': [],
    },
    'Dark Purplish Blue': {
        'color_range': [ColorRange.Blue],
        'analogous': ['Navy'],
    },
    'Very Pale Purplish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Grey],
        'analogous': [],
    },
    'Pale Purplish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Grey],
        'analogous': [],
    },
    'Grayish Purplish Blue': {
        'color_range': [ColorRange.Blue, ColorRange.Grey],
        'analogous': [],
    },
    'Vivid Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Amethyst', 'Violet'],
    },
    'Brilliant Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Amethyst', 'Iris', 'Violet'],
    },
    'Strong Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Violet'],
    },
    'Deep Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Violet'],
    },
    'Very Light Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Violet'],
    },
    'Light Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Lavender', 'Violet'],
    },
    'Moderate Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Violet'],
    },
    'Dark Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Violet'],
    },
    'Very Pale Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Lavender', 'Violet'],
    },
    'Pale Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Violet'],
    },
    'Grayish Violet': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Violet'],
    },
    'Vivid Purple': {
        'color_range': [ColorRange.Pink, ColorRange.Purple],
        'analogous': ['Magenta'],
    },
    'Brilliant Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Orchid'],
    },
    'Strong Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': [],
    },
    'Deep Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': [],
    },
    'Very Deep Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': [],
    },
    'Very Light Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': [],
    },
    'Light Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Lilac', 'Wisteria'],
    },
    'Moderate Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': [],
    },
    'Dark Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': [],
    },
    'Very Dark Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': [],
    },
    'Very Pale Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': ['Lavender'],
    },
    'Pale Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': [],
    },
    'Grayish Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': [],
    },
    'Dark Grayish Purple': {
        'color_range': [ColorRange.Purple],
        'analogous': [],
    },
    'Blackish Purple': {
        'color_range': [ColorRange.Purple, ColorRange.Black],
        'analogous': [],
    },
    'Purplish White': {
        'color_range': [ColorRange.Grey, ColorRange.White],
        'analogous': [],
    },
    'Light Purplish Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Purplish Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Dark Purplish Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Purplish Black': {
        'color_range': [ColorRange.Black, ColorRange.Grey],
        'analogous': [],
    },
    'Vivid Reddish Purple': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Magenta', 'Rose'],
    },
    'Strong Reddish Purple': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Magenta'],
    },
    'Deep Reddish Purple': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Magenta'],
    },
    'Very Deep Reddish Purple': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Magenta'],
    },
    'Light Reddish Purple': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Magenta', 'Plum'],
    },
    'Moderate Reddish Purple': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Magenta'],
    },
    'Dark Reddish Purple': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Magenta'],
    },
    'Very Dark Reddish Purple': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Magenta'],
    },
    'Pale Reddish Purple': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Grayish Reddish Purple': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Brilliant Purplish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Strong Purplish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Deep Purplish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Light Purplish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Rose'],
    },
    'Moderate Purplish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Dark Purplish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Pale Purplish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': [],
    },
    'Grayish Purplish Pink': {
        'color_range': [ColorRange.Pink],
        'analogous': ['Pink Lavender'],
    },
    'Vivid Purplish Red': {
        'color_range': [ColorRange.Pink, ColorRange.Red],
        'analogous': ['Magenta'],
    },
    'Strong Purplish Red': {
        'color_range': [ColorRange.Pink, ColorRange.Red],
        'analogous': ['Magenta'],
    },
    'Deep Purplish Red': {
        'color_range': [ColorRange.Pink, ColorRange.Red],
        'analogous': ['Magenta'],
    },
    'Very Deep Purplish Red': {
        'color_range': [ColorRange.Pink, ColorRange.Red],
        'analogous': ['Magenta'],
    },
    'Moderate Purplish Red': {
        'color_range': [ColorRange.Pink, ColorRange.Red],
        'analogous': ['Magenta'],
    },
    'Dark Purplish Red': {
        'color_range': [ColorRange.Pink, ColorRange.Red],
        'analogous': ['Magenta'],
    },
    'Very Dark Purplish Red': {
        'color_range': [ColorRange.Pink, ColorRange.Red],
        'analogous': ['Magenta'],
    },
    'Light Grayish Purplish Red': {
        'color_range': [ColorRange.Pink, ColorRange.Red],
        'analogous': [],
    },
    'Grayish Purplish Red': {
        'color_range': [ColorRange.Pink, ColorRange.Red],
        'analogous': ['Lavender'],
    },
    'White': {
        'color_range': [ColorRange.White],
        'analogous': [],
    },
    'Light Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Medium Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Dark Gray': {
        'color_range': [ColorRange.Grey],
        'analogous': [],
    },
    'Black': {
        'color_range': [ColorRange.Black],
        'analogous': ['Ebony'],
    },
}

ISCC_NBS_LUMINENT_DESCRIPTORS = [
    'Brilliant',
    'Dark',
    'Deep',
    'Light',
    'Medium',
    'Moderate',
    'Pale',
    'Strong',
    'Very',
    'Vivid',
]

ISCC_NBS_HUE_DESCRIPTORS = [
    'Blackish',
    'Bluish',
    'Brownish',
    'Grayish',
    'Greenish',
    'Pinkish',
    'Purplish',
    'Reddish',
    'Yellowish'
]