try:
    from ORM.ORM_session import engine, ORM_session
    from ORM.base import Model
    from ORM.tables import *
except ImportError:
    from ORM_session import engine, ORM_session
    from base import Model
    from tables import *

category_info = [
    'Compost',
    'Decorations',
    'Edging',
    'Fertiliser',
    'Mulch',
    'Paving',
    'Pots',
    'Retaining Wall',
    'Sand',
    'Seeds',
    'Soil',
    'Turf',
    'Fabric',
]
product_info = [
    ['Loam Topsoil', 'Loam Topsoil is comprised of a mixture of clay, sand and silt that avoid the extremes of clay or sandy soils and are fertile, well-drained and easily worked.', None, None, 'per cubic metre', 50.00, 200, 11, 'static/loam.jpeg'],
    ['Garden Soil Mix', 'A pre-blended soil, often used as a substitute for topsoil in gardens, that contains a higher percentage of organic matter than typical garden soil. It''s designed to provide an ideal growing environment for plants by enhancing drainage, water retention, and nutrient availability.', None, None, 'per cubic metre', 50.00, 200, 11, 'static/garden_soil.jpg'],
    ['Compost', 'This product has been developed by horticultural experts to provide your plants with the ideal moisture and nutrients. It contains Gypsum to improve soil texture and provides plants with calcium. Made from composted materials. Contains no animal by-products (manures or blood & bone) so has no odour, just a fresh earthy smell.', None, None, 'per cubic metre', 50.00, 200, 1, 'static/compost.jpeg'],
    ['Organic Mulch', 'Contains grasses, leaves, straw, shredded bark, pine needles and compost, helping condition the soil, even inviting earthworms to naturally aerate the soil. This helps reduce soil compaction.', None, None, 'per cubic metre', 60.00, 200, 5, 'static/mulch.jpeg'],
    ['Pine Bark Mulch', 'Pine Bark Mulch is an attractive timber mulch for landscaping garden beds and pots. It is screened and graded to ensure consistent sized chips. It helps prevent weed growth, contains moisture, and helps regulate soil temperature.', None, None, 'per cubic metre', 12.99, 200, 5, 'static/pine_bark_mulch.jpg'],
    ['River Pebbles', 'These natural river stones and pebbles are a roundish shape, tumbled by water flow. They come in a mix of colours; mostly brown to beige and sometimes with charcoal tones. Round River stones are available in 6 different sizes, all of which look great in garden beds. The smaller 7mm, 10 mm and 20 mm sizes are suitable for driveways and paths.', None, 20.00, 'per bag', 80.00, 100, 2, 'static/pebbles.jpg'],
    ['Crushed Granite', 'The soft, warm gold colour of this decomposed granite makes it ideal for creating paths and driveways that blend into the landscape. This is a compactable product that can be stabilised with cement to give a hard surface if laid correctly.', None, None, 'per tonne', 50.00, 50, 6, 'static/crushed_granite.jpg'],
    ['Road Base', 'A well graded material consisting of various sized particles containing coarse and fine aggregate to enable compaction. Road Base can be used for many of your compacting jobs around the home, such as paths, car parks, under slabs, driveways under water, and walkways.', None, None, 'per tonne', 60.00, 50, 6, 'static/road_base.jpg'],
    ['Washed Sand', 'Suitable for use as a top dressing on cored lawns, adding drainage to garden soils, and as a bedding sand.', None, None, 'per tonne', 60.00, 50, 9, 'static/washed_sand.webp'],
    ['Paver Sand', 'Coarse sand perfect for garden paths, bedding pavers, and under slabs.', '290x100x500mm', 20.00, 'per bag', 12.99, 50, 9, 'static/paver_sand.png'],
    ['Concrete Pavers', 'Suitable for use as stepping stones, garden paths, and edging.', '400x400x20mm', 8.8, 'per piece', 9.99, 50, 6, 'static/concrete_pavers.jpeg'],
    ['Retaining Wall Blocks', 'A standard split face finish with chamfered edges at the top and both sides. Perfect for modern dry stacked retaining walls where a clean finish is desired.', '340x140x200mm', 20.00, 'per piece', 12.00, 200, 8, 'static/stone_blocks.jpg'],
    ['Garden Edging', 'This Galvanised Stainless Steel is rust, mould, and weather resistant, its sleek design perfect for any modern garden. This product contains 6 items.', '160x1000x1mm', None, 'per piece', 20.00, 50, 3, 'static/garden_edging.jpg'],
    ['Turf (Wintergreen Couch)', 'Wintergreen Couch Grass is a great all round turf for full sun areas. It has a fine soft leaf and a lovely green colour. It is also hard wearing and has excellent drought tolerance. If looked after well with fertilising, watering, weeding and mowing it produces a beautiful finish to any full sun area.', None, None, 'per square metre', 1.99, 500, 12, 'static/wintergreen_turf.jpg'],
    ['Turf (Augusta Zoysia)', 'Augusta Zoysia boasts a high shade tolerance, very high drought tolerance, and high wear tolerancery, making it low maintenance. It is Attractive dark green colour with a fine leaf making it soft to touch and underfoot.', None, None, 'per square metre', 6.89, 500, 12, 'static/augusta_turf.jpg'],
    ['Grass Seed (Buffalo)', 'Buffalo Grass Seed is a hardy, drought tolerant grass that is ideal for sunny areas. It has a soft leaf and a lovely green colour. It is also hard wearing and has excellent drought tolerance.', None, 0.5, 'per bag', 20.00, 100, 10, 'static/grass_seeds.jpeg'],
    ['Fertiliser', 'A special combination of advanced fertiliser technology that gives your plants an instant release of nutrients, then continues feeding for up to 12 months (depending on temperature and soil moisture). Contains the best of  plant boosters -  blood and bone,  phosphorus and  potash for extra strength and plant colour, particularly fruits and vegetables.', '320x90x530mm', 15.00, 'per bag', 20.50, 50, 4, 'static/fertiliser.jpeg'],
    ['Landscaping Fabric', 'Landscaping Fabric is used for soil drainage, erosion control, soil layer separation, and other landscaping applications.', '0.9x15m', 8.00, 'per roll', 15.00, 50, 13, 'static/fabric.jpg'],
    ['Ceramic Pot', 'Ceramic pot perfect for holding plants. 25.5L Volume.', '330x221x330mm', 2.00, 'per piece', 10.00, 50, 7, 'static/pot.jpeg'],
    ['Landscape Lighting Kit', 'The spike light can be adjusted on a 90-degree angle that shines at 36 degrees and has a surface or spike mounting option. The light comes attached with 2 cables measuring 2m with fittings at the ends. To power, just connect the spike light in line with the wifi controller and driver.', '70x45x45mm', None, 'per piece', 35.00, 50, 2, 'static/light.jpeg']
]

roles = [
    [1, 'admin'],
    [2, 'user']
]

# Create the database tables
# This will create all tables defined in the models (base and tables in tables)
Model.metadata.drop_all(engine)
Model.metadata.create_all(engine)

for element in category_info:
    ORM_session.add(Category(
        category=element
    ))

for role in roles:
    ORM_session.add(Role(
        role=role[0],
        description=role[1]
    ))

for product in product_info:
    ORM_session.add(Product(
        name=product[0],
        description=product[1],
        dimensions=product[2],
        weight=product[3],
        unit=product[4],
        price=product[5],
        stock_level=product[6],
        category=product[7],
        image=product[8]
    ))

#adds an admin user
ORM_session.add(User(
    username='admin',
    password='$2b$12$lN4SyYuCp.wY1BhEKDy6AO7OVK4.VIqnQy8h6RDx1HBTtLsPT0xi2',
    securityQ1="What is your sibling's middle name?",
    securityQ2="What was the name of your first stuffed toy?",
    securityQ3="What was the name of the sporting team you first supported?",
    securityA1="$2b$12$6/sUhc.8ssyJrBBwkwQepeJWdI/TAYsnCQCcBUgLpUHwGxF63N1T2",
    securityA2="$2b$12$RcqOz./tQsAmJGQss3l/HuzUP0zYHaqaHHj2G4RScSAWwEFRtWMRy",
    securityA3="$2b$12$v7wYo5X5vtaFqWMFYU0Nk.2b9.JXruxiEtr2ZfR18M.gtSxD6nZqe",
    address='gAAAAABoWJu2Vl8r4yvQcSZdelxsNrbwqavSaY3QTE9SvhRZ_7OeXLuYvh4pOcR0Vcco8loUx3OxAB64YE80Z4fecAJT-aa1_Q==',
    phone_number="gAAAAABoWJu2kzb9-kLyR8mJZkPFxJHUkALZktA1TgiWNaUY6y4QuDNjZXtt8Eq3eHBadIFzndKJ_Heb1txOVlPdtOEkQwB9cw==",
    picture="static/profile_pictures/1.jpg",
    role=1,
    attempts=5,
    last_attempt=1750637494.40712
))
ORM_session.commit()
ORM_session.close()

