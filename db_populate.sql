USE `agrihire`;

INSERT INTO location_regions (`name`) VALUES
('Northland'),
('Auckland'),
('Waikato'),
('Bay of Plenty'),
('Gisborne'),
('Hawke''s Bay'),
('Taranaki'),
('Manawatū-Whanganui'),
('Wellington'),
('Tasman'),
('Nelson'),
('Marlborough'),
('West Coast'),
('Canterbury'),
('Otago'),
('Southland');

INSERT INTO location_districts (`name`, `region_id`) VALUES
-- Northland Region (ID: 1)
('Whangārei', 1),
('Far North', 1),
('Kaipara', 1),
-- Auckland Region (ID: 2)
('Auckland Council', 2),
-- Waikato Region (ID: 3)
('Thames-Coromandel', 3),
('Hauraki', 3),
('Waikato', 3),
('Matamata-Piako', 3),
('Hamilton City', 3),
('Waipā', 3),
('Ōtorohanga', 3),
('South Waikato', 3),
('Waitomo', 3),
('Taupō', 3),
-- Bay of Plenty Region (ID: 4)
('Western Bay of Plenty', 4),
('Tauranga City', 4),
('Rotorua Lakes', 4),
('Whakatāne', 4),
('Kawerau', 4),
('Ōpōtiki', 4),
-- Gisborne Region (ID: 5)
('Gisborne', 5),
-- Hawke's Bay Region (ID: 6)
('Wairoa', 6),
('Hastings', 6),
('Napier City', 6),
('Central Hawke''s Bay', 6),
-- Taranaki Region (ID: 7)
('New Plymouth', 7),
('Stratford', 7),
('South Taranaki', 7),
-- Manawatū-Whanganui Region (ID: 8)
('Ruapehu', 8),
('Whanganui', 8),
('Rangitikei', 8),
('Manawatū', 8),
('Palmerston North City', 8),
('Tararua', 8),
('Horowhenua', 8),
-- Wellington Region (ID: 9)
('Kāpiti Coast', 9),
('Porirua City', 9),
('Upper Hutt City', 9),
('Hutt City', 9),
('Wellington City', 9),
('Masterton', 9),
('Carterton', 9),
('South Wairarapa', 9),
-- Tasman Region (ID: 10)
('Tasman', 10),
-- Nelson Region (ID: 11)
('Nelson City', 11),
-- Marlborough Region (ID: 12)
('Marlborough', 12),
-- West Coast Region (ID: 13)
('Buller', 13),
('Grey', 13),
('Westland', 13),
-- Canterbury Region (ID: 14)
('Kaikōura', 14),
('Hurunui', 14),
('Waimakariri', 14),
('Christchurch City', 14),
('Selwyn', 14),
('Ashburton', 14),
('Timaru', 14),
('Mackenzie', 14),
('Waimate', 14),
-- Otago Region (ID: 15)
('Central Otago', 15),
('Queenstown-Lakes', 15),
('Clutha', 15),
('Waitaki', 15),
('Dunedin City', 15),
-- Southland Region (ID: 16)
('Southland', 16),
('Gore', 16),
('Invercargill City', 16);

-- ===============================
-- Northland Region
-- ===============================

-- Whangārei District (district_id = 1)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Whangārei Central', 1),
('Kamo', 1),
('Onerahi', 1),
('Tikipunga', 1),
('Maunu', 1),
('Raumanga', 1),
('Morningside', 1),
('Regent', 1),
('Kensington', 1),
('Riverside', 1);

-- Far North District (district_id = 2)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Kaitaia', 2),
('Kerikeri', 2),
('Kaikohe', 2),
('Paihia', 2),
('Kawakawa', 2),
('Moerewa', 2),
('Ahipara', 2),
('Coopers Beach', 2),
('Mangonui', 2),
('Ōpononi', 2),
('Ōmāpere', 2),
('Houhora', 2);

-- Kaipara District (district_id = 3)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Dargaville', 3),
('Mangawhai Heads', 3),
('Mangawhai Village', 3),
('Maungaturoto', 3),
('Ruawai', 3),
('Kaiwaka', 3);

-- ===============================
-- Auckland Region
-- ===============================

-- Auckland Council (district_id = 4)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Auckland CBD', 4),
('Ponsonby', 4),
('Grey Lynn', 4),
('Mt Eden', 4),
('Epsom', 4),
('Remuera', 4),
('Parnell', 4),
('Takapuna', 4),
('Albany', 4),
('Manukau', 4),
('Papakura', 4),
('Ōtāhuhu', 4),
('Henderson', 4),
('Glen Innes', 4);

-- ===============================
-- Waikato Region
-- ===============================

-- Thames-Coromandel (district_id = 5)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Thames', 5),
('Whitianga', 5),
('Coromandel Town', 5),
('Whangamatā', 5);

-- Hauraki (district_id = 6)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Paeroa', 6),
('Waihi', 6),
('Ngātea', 6);

-- Waikato (district_id = 7)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Huntly', 7),
('Ngaruawahia', 7),
('Tuakau', 7),
('Raglan', 7);

-- Matamata-Piako (district_id = 8)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Matamata', 8),
('Morrinsville', 8),
('Te Aroha', 8);

-- Hamilton City (district_id = 9)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Hamilton East', 9),
('Hamilton West', 9),
('Frankton', 9),
('Rototuna', 9),
('Dinsdale', 9),
('Forest Lake', 9);

-- Waipā (district_id = 10)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Cambridge', 10),
('Te Awamutu', 10);

-- Ōtorohanga (district_id = 11)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Ōtorohanga', 11);

-- South Waikato (district_id = 12)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Tokoroa', 12),
('Putāruru', 12);

-- Waitomo (district_id = 13)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Te Kūiti', 13);

-- Taupō (district_id = 14)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Taupō', 14),
('Tūrangi', 14);

-- ===============================
-- Bay of Plenty Region
-- ===============================

-- Western Bay of Plenty (district_id = 15)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Katikati', 15),
('Te Puke', 15),
('Tauranga', 15);

-- Tauranga City (district_id = 16)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Tauranga CBD', 16),
('Mount Maunganui', 16),
('Papamoa', 16),
('Otumoetai', 16),
('Maungatapu', 16);

-- Rotorua Lakes (district_id = 17)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Rotorua Central', 17),
('Fenton Park', 17),
('Ngongotahā', 17);

-- Whakatāne (district_id = 18)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Whakatāne', 18),
('Ōhope', 18),
('Edgecumbe', 18);

-- Kawerau (district_id = 19)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Kawerau', 19);

-- Ōpōtiki (district_id = 20)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Ōpōtiki', 20);

-- ===============================
-- Gisborne Region
-- ===============================

-- Gisborne (district_id = 21)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Gisborne Central', 21),
('Kaiti', 21),
('Makaraka', 21),
('Mangapapa', 21);

-- ===============================
-- Hawke's Bay Region
-- ===============================

-- Wairoa (district_id = 22)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Wairoa', 22);

-- Hastings (district_id = 23)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Hastings', 23),
('Havelock North', 23),
('Flaxmere', 23);

-- Napier City (district_id = 24)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Napier Central', 24),
('Taradale', 24),
('Ahuriri', 24);

-- Central Hawke's Bay (district_id = 25)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Waipukurau', 25),
('Waipawa', 25);

-- ===============================
-- Taranaki Region
-- ===============================

-- New Plymouth (district_id = 26)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('New Plymouth Central', 26),
('Bell Block', 26),
('Inglewood', 26),
('Waitara', 26);

-- Stratford (district_id = 27)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Stratford', 27);

-- South Taranaki (district_id = 28)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Hāwera', 28),
('Eltham', 28),
('Patea', 28);

-- ===============================
-- Manawatū-Whanganui Region
-- ===============================

-- Ruapehu (district_id = 29)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Taumarunui', 29),
('Ōhākune', 29),
('National Park Village', 29);

-- Whanganui (district_id = 30)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Whanganui Central', 30),
('Durie Hill', 30),
('Aramoho', 30);

-- Rangitīkei (district_id = 31)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Marton', 31),
('Bulls', 31),
('Taihape', 31);

-- Manawatū (district_id = 32)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Feilding', 32),
('Halcombe', 32),
('Kimbolton', 32);

-- Palmerston North City (district_id = 33)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Palmerston North Central', 33),
('Terrace End', 33),
('Hokowhitu', 33),
('Awapuni', 33),
('Roslyn', 33);

-- Tararua (district_id = 34)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Dannevirke', 34),
('Pahiatua', 34);

-- Horowhenua (district_id = 35)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Levin', 35),
('Foxton', 35),
('Shannon', 35);

-- ===============================
-- Wellington Region
-- ===============================

-- Kāpiti Coast (district_id = 36)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Paraparaumu', 36),
('Waikanae', 36),
('Ōtaki', 36);

-- Porirua City (district_id = 37)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Porirua Central', 37),
('Whitby', 37),
('Titahi Bay', 37);

-- Upper Hutt City (district_id = 38)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Upper Hutt Central', 38),
('Trentham', 38),
('Heretaunga', 38);

-- Hutt City (district_id = 39)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Lower Hutt Central', 39),
('Petone', 39),
('Wainuiomata', 39),
('Naenae', 39),
('Avalon', 39);

-- Wellington City (district_id = 40)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Wellington Central', 40),
('Karori', 40),
('Miramar', 40),
('Johnsonville', 40),
('Tawa', 40),
('Kilbirnie', 40);

-- Masterton (district_id = 41)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Masterton Central', 41),
('Solway', 41),
('Lansdowne', 41);

-- Carterton (district_id = 42)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Carterton', 42);

-- South Wairarapa (district_id = 43)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Martinborough', 43),
('Greytown', 43),
('Featherston', 43);

-- ===============================
-- Tasman Region
-- ===============================

-- Tasman (district_id = 44)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Richmond', 44),
('Motueka', 44),
('Māpua', 44);

-- ===============================
-- Nelson Region
-- ===============================

-- Nelson City (district_id = 45)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Nelson Central', 45),
('Stoke', 45),
('Tahunanui', 45);

-- ===============================
-- Marlborough Region
-- ===============================

-- Marlborough (district_id = 46)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Blenheim', 46),
('Springlands', 46),
('Picton', 46),
('Renwick', 46);

-- ===============================
-- West Coast Region
-- ===============================

-- Buller (district_id = 47)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Westport', 47),
('Karamea', 47);

-- Grey (district_id = 48)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Greymouth', 48),
('Runanga', 48),
('Cobden', 48);

-- Westland (district_id = 49)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Hokitika', 49),
('Whataroa', 49),
('Franz Josef / Waiau', 49);

-- ===============================
-- Canterbury Region
-- ===============================

-- Kaikōura (district_id = 50)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Kaikōura', 50);

-- Hurunui (district_id = 51)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Amberley', 51),
('Hanmer Springs', 51),
('Cheviot', 51);

-- Waimakariri (district_id = 52)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Rangiora', 52),
('Kaiapoi', 52),
('Oxford', 52);

-- Christchurch City (district_id = 53)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Addington', 53),
('Riccarton', 53),
('Fendalton', 53),
('Papanui', 53),
('Merivale', 53),
('St Albans', 53),
('Sydenham', 53),
('Linwood', 53),
('Halswell', 53),
('Hornby', 53),
('New Brighton', 53),
('Sumner', 53),
('Cashmere', 53),
('Aranui', 53),
('Bishopdale', 53),
('Burnside', 53),
('Avonhead', 53),
('St Martins', 53),
('Woolston', 53),
('Beckenham', 53);

-- Selwyn (district_id = 54)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Rolleston', 54),
('Lincoln', 54),
('Darfield', 54);

-- Ashburton (district_id = 55)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Ashburton', 55),
('Tinwald', 55),
('Hampstead', 55);

-- Timaru (district_id = 56)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Timaru', 56),
('Washdyke', 56),
('Pleasant Point', 56);

-- Mackenzie (district_id = 57)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Twizel', 57),
('Lake Tekapo', 57),
('Fairlie', 57);

-- Waimate (district_id = 58)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Waimate', 58);

-- ===============================
-- Otago Region
-- ===============================

-- Central Otago (district_id = 59)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Alexandra', 59),
('Cromwell', 59);

-- Queenstown-Lakes (district_id = 60)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Queenstown', 60),
('Wānaka', 60),
('Arrowtown', 60);

-- Clutha (district_id = 61)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Balclutha', 61),
('Kaitangata', 61),
('Milton', 61);

-- Waitaki (district_id = 62)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Ōamaru', 62),
('Hampden', 62),
('Palmerston', 62);

-- Dunedin City (district_id = 63)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Dunedin Central', 63),
('Mosgiel', 63),
('Port Chalmers', 63),
('St Clair', 63),
('St Kilda', 63),
('South Dunedin', 63);

-- ===============================
-- Southland Region
-- ===============================

-- Southland (district_id = 64)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Gore', 64),
('Winton', 64),
('Riverton', 64),
('Te Anau', 64);

-- Gore (district_id = 65)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Gore', 65),
('Mataura', 65);

-- Invercargill City (district_id = 66)
INSERT INTO location_suburbs (`name`, `district_id`) VALUES
('Invercargill Central', 66),
('Bluff', 66),
('Strathern', 66),
('Glengarry', 66);

-- INSERT INTO location_street_details(`street_name`, `city`, `zip`, `suburb_id`) VALUES
-- ('Queen Street', 'Auckland', '1010', 29),
-- ('Kamo Road', 'Whangārei', '0110', 1),
-- ('Rotorua Central Road', 'Rotorua', '3010', 17),
-- ('Cambridge Street', 'Cambridge', '3434', 10),
-- ('Merivale Avenue', 'Christchurch', '8014', 53);

INSERT INTO users (`username`, `first_name`, `last_name`, `email`, `mobile`, `password_hash`, `profile_image`) VALUES
('jdoe', 'John', 'Doe', 'john.doe@example.com', '021-123-4567', '$2b$12$xZFQiW644kBUuH/Wedap1eOYbBBqmnGDi3BOcAXbhAJffHYTu.Pvi', 'https://picsum.photos/200?random=1'),
('q1', 'Frank', 'Clark', 'frank.clark@example.com', '021-789-0123', '$2b$12$xZFQiW644kBUuH/Wedap1eOYbBBqmnGDi3BOcAXbhAJffHYTu.Pvi', 'https://picsum.photos/200?random=7'),
('asmith', 'Alice', 'Smith', 'alice.smith@example.com', '021-234-5678', '$2b$12$xZFQiW644kBUuH/Wedap1eOYbBBqmnGDi3BOcAXbhAJffHYTu.Pvi', 'https://picsum.photos/200?random=2'),
('bjones', 'Bob', 'Jones', 'bob.jones@example.com', '021-345-6789', '$2b$12$xZFQiW644kBUuH/Wedap1eOYbBBqmnGDi3BOcAXbhAJffHYTu.Pvi', 'https://picsum.photos/200?random=3'),
('cwilson', 'Charlie', 'Wilson', 'charlie.wilson@example.com', '021-456-7890', '$2b$12$xZFQiW644kBUuH/Wedap1eOYbBBqmnGDi3BOcAXbhAJffHYTu.Pvi', 'https://picsum.photos/200?random=4'),
('dlee', 'David', 'Lee', 'david.lee@example.com', '021-567-8901', '$2b$12$xZFQiW644kBUuH/Wedap1eOYbBBqmnGDi3BOcAXbhAJffHYTu.Pvi', 'https://picsum.photos/200?random=5'),
('ewatson', 'Emma', 'Watson', 'emma.watson@example.com', '021-678-9012', '$2b$12$xZFQiW644kBUuH/Wedap1eOYbBBqmnGDi3BOcAXbhAJffHYTu.Pvi', 'https://picsum.photos/200?random=6');


INSERT INTO equipment_categories (name) VALUES
('Tractors'),
('Attachments'),
('Tillage'),
('Soil Preparation'),
('Planting'),
('Seeding'),
('Harvesters'),
('Balers'),
('Sprayers'),
('Spreaders'),
('Irrigation'),
('Hay'),
('Forage'),
('Livestock'),
('Fencing'),
('Loading & Material Handling'),
('Storage & Silos'),
('Workshop Equipment');

INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(1, 'Sub-Compact Tractors'),
(1, 'Compact Tractors'),
(1, 'Utility Tractors'),
(1, 'Row-Crop Tractors'),
(1, 'Articulated Tractors'),
(1, '4WD Tractors');

-- Attachments (category_id = 2)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(2, 'Front-End Loaders'),
(2, 'Post-Hole Diggers'),
(2, 'Rotary Cutters / Slashers'),
(2, 'Bale Spears'),
(2, 'Pallet Forks'),
(2, 'Grapple Attachments');

-- Tillage (category_id = 3)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(3, 'Mouldboard Ploughs'),
(3, 'Disc Ploughs'),
(3, 'Chain Harrows'),
(3, 'Disc Harrows'),
(3, 'Power Harrows'),
(3, 'Rotary Tillers'),
(3, 'Field Cultivators'),
(3, 'Subsoilers'),
(3, 'Land Rollers');

-- Soil Preparation (category_id = 4)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(4, 'Bed Formers'),
(4, 'Fertilizer Spreaders (Solid/Liquid)');

-- Planting (category_id = 5)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(5, 'Seed Drills'),
(5, 'Planters'),
(5, 'Transplanters'),
(5, 'Potato Planters');

-- Seeding (category_id = 6)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(6, 'Broadcast Seeders'),
(6, 'Air Seeders');

-- Harvesters (category_id = 7)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(7, 'Combine Harvesters'),
(7, 'Forage Harvesters'),
(7, 'Potato Harvesters'),
(7, 'Grape Harvesters'),
(7, 'Corn / Maize Harvesters'),
(7, 'Sugarcane Harvesters');

-- Balers (category_id = 8)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(8, 'Round Balers'),
(8, 'Square Balers'),
(8, 'Large Square Balers');

-- Sprayers (category_id = 9)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(9, 'Field Sprayers'),
(9, 'Orchard Sprayers'),
(9, 'Boom Sprayers'),
(9, 'Mist Blowers');

-- Spreaders (category_id = 10)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(10, 'Fertilizer Spreaders'),
(10, 'Manure Spreaders'),
(10, 'Lime Spreaders');

-- Irrigation (category_id = 11)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(11, 'Pumps'),
(11, 'Pivots'),
(11, 'Drip Irrigation Systems'),
(11, 'Hoses & Fittings'),
(11, 'Traveling Irrigation Systems');

-- Hay (category_id = 12)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(12, 'Mowers'),
(12, 'Hay Rakes'),
(12, 'Hay Tedders'),
(12, 'Hay Conditioners');

-- Forage (category_id = 13)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(13, 'Silage Wrappers'),
(13, 'Forage Wagons'),
(13, 'Feed Mixers');

-- Livestock (category_id = 14)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(14, 'Feed Mixers'),
(14, 'Shearing Equipment'),
(14, 'Cattle Crushes'),
(14, 'Milking Machines'),
(14, 'Animal Feeders'),
(14, 'Water Troughs');

-- Fencing (category_id = 15)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(15, 'Post Drivers'),
(15, 'Electric Fencing Equipment'),
(15, 'Wire Stretchers');

-- Loading & Material Handling (category_id = 16)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(16, 'Telehandlers'),
(16, 'Pallet Jacks'),
(16, 'Forklifts'),
(16, 'Cranes / Hoists');

-- Storage & Silos (category_id = 17)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(17, 'Grain Silos'),
(17, 'Feed Bins'),
(17, 'Water Tanks');

-- Workshop Equipment (category_id = 18)
INSERT INTO equipment_subcategories (`category_id`, `name`) VALUES
(18, 'Welders'),
(18, 'Generators'),
(18, 'Air Compressors'),
(18, 'Hydraulic Jacks');


-- Equipment 1: Excavator
INSERT INTO equipments (
    `name`, `make`, `model`, `year`, `category_id`, `sub_category_id`, `user_id`,
    `description`, `price`, `price_modal`, `region_id`, `district_id`, `suburb_id`,
    `street_name`, `city`, `zip`, `latitude`, `longitude`,
    `height`, `length`, `width`, `weight`,
    `is_public`, `is_hired`, `status`
) VALUES
(
    'John Deere Tractor', 'John Deere', 'X350', 2019, 1, 2, 1,
    'Reliable lawn tractor.', 150, 'per_hour', 1, 1, 1,
    '21 Greenfield St', 'Auckland', '1010', -36.8485, 174.7633,
    1, 3, 2, 400,
    TRUE, FALSE, 'listed'
),
(
    'Stihl Chainsaw', 'Stihl', 'MS 250', 2020, 3, 5, 1,
    'Powerful chainsaw.', 70, 'per_day', 1, 1, 1,
    '21 Greenfield St', 'Auckland', '1010', -36.8485, 174.7633,
    0, 2, 1, 6,
    TRUE, FALSE, 'listed'
),
(
    'Caterpillar Excavator', 'Caterpillar', '320D', 2018, 1, 2, 2,
    'Heavy duty excavator.', 500, 'per_day', 2, 3, 3,
    '123 Industrial Ave', 'Wellington', '6011', -41.2865, 174.7762,
    3, 9, 4, 20000,
    TRUE, FALSE, 'listed'
),
(
    'Honda Generator', 'Honda', 'EU2200i', 2021, 3, 5, 2,
    'Portable generator.', 100, 'per_hour', 2, 3, 3,
    '456 Suburb Rd', 'Wellington', '6011', -41.2865, 174.7762,
    1, 2, 2, 80,
    TRUE, FALSE, 'listed'
),
(
    'Bosch Power Drill', 'Bosch', 'X123', 2020, 5, 8, 3,
    'Electric power drill.', 20, 'per_hour', 3, 5, 5,
    '789 Downtown St', 'Christchurch', '8011', -43.5321, 172.6362,
    0, 1, 1, 3,
    TRUE, FALSE, 'listed'
),
(
    'Makita Circular Saw', 'Makita', '5605R', 2019, 5, 9, 3,
    'Circular saw.', 30, 'per_day', 3, 5, 5,
    '789 Downtown St', 'Christchurch', '8011', -43.5321, 172.6362,
    0, 1, 1, 5,
    TRUE, FALSE, 'listed'
),
(
    'Hitachi Hammer Drill', 'Hitachi', 'DH24PB3', 2019, 4, 7, 4,
    'High performance hammer drill.', 45, 'per_hour', 4, 6, 6,
    '12 Mountain Rd', 'Hamilton', '3204', -37.7833, 175.2833,
    0, 2, 1, 4,
    TRUE, FALSE, 'listed'
),
(
    'Echo Leaf Blower', 'Echo', 'PB-580T', 2020, 6, 10, 4,
    'Powerful leaf blower for lawns.', 25, 'per_day', 4, 6, 6,
    '12 Mountain Rd', 'Hamilton', '3204', -37.7833, 175.2833,
    0, 1, 1, 5,
    TRUE, FALSE, 'listed'
),
(
    'Toro Lawn Mower', 'Toro', 'Recycler 20340', 2021, 2, 3, 5,
    'Efficient lawn mower.', 60, 'per_day', 5, 7, 7,
    '88 Riverside Dr', 'Dunedin', '9016', -45.8742, 170.5036,
    1, 4, 2, 350,
    TRUE, FALSE, 'listed'
),
(
    'Black & Decker Sander', 'Black & Decker', 'BDEQS300', 2020, 5, 8, 5,
    'Electric hand sander.', 15, 'per_hour', 5, 7, 7,
    '88 Riverside Dr', 'Dunedin', '9016', -45.8742, 170.5036,
    0, 1, 1, 2,
    TRUE, FALSE, 'listed'
),
(
    'DeWalt Cordless Drill', 'DeWalt', 'DCD771C2', 2022, 5, 8, 6,
    'Cordless drill with lithium battery.', 50, 'per_hour', 6, 8, 8,
    '45 Forest Ln', 'Napier', '4110', -39.4928, 176.912,
    0, 2, 1, 5,
    TRUE, FALSE, 'listed'
),
(
    'Hitachi Circular Saw', 'Hitachi', 'C7SB3', 2018, 5, 9, 6,
    'Lightweight circular saw.', 35, 'per_day', 6, 8, 8,
    '45 Forest Ln', 'Napier', '4110', -39.4928, 176.912,
    0, 1, 1, 6,
    TRUE, FALSE, 'listed'
);

INSERT INTO safety_options (`name`) VALUES 
('Safety Harness Required'),
('Hard Hat Zone'),
('High Visibility Vest'),
('Certified Operator Only'),
('Emergency Stop Available'),
('Safety Guards Installed'),
('Lockout/Tagout Required'),
('Safety Training Mandatory');

INSERT INTO equipment_safety_options (`equipment_id`, `safety_id`) VALUES
(1, 1),
(1, 3),
(2, 2),
(3, 1),
(3, 2),
(4, 3),
(5, 2),
(6, 1),
(7, 3),
(8, 1),
(9, 2),
(10, 3),
(11, 1),
(12, 2);

INSERT INTO `equipment_files` (`equipment_id`, `file_path`, `file_type`, `user_id`) VALUES
(1, 'images/equipment/1_image1.jpg', 'image', 1),
(1, 'docs/equipment/1_safety_doc.pdf', 'safety_doc', 1),
(2, 'images/equipment/2_image1.jpg', 'image', 1),
(3, 'images/equipment/3_image1.jpg', 'image', 2),
(3, 'docs/equipment/3_safety_doc.pdf', 'safety_doc', 2),
(4, 'images/equipment/4_image1.jpg', 'image', 2),
(5, 'images/equipment/5_image1.jpg', 'image', 3),
(6, 'docs/equipment/6_safety_doc.pdf', 'safety_doc', 3),
(7, 'images/equipment/7_image1.jpg', 'image', 4),
(8, 'docs/equipment/8_safety_doc.pdf', 'safety_doc', 4),
(9, 'images/equipment/9_image1.jpg', 'image', 5),
(10, 'docs/equipment/10_safety_doc.pdf', 'safety_doc', 5),
(11, 'images/equipment/11_image1.jpg', 'image', 6),
(12, 'docs/equipment/12_safety_doc.pdf', 'safety_doc', 6);

-- Equipment Requests
INSERT INTO `equipment_requests` (
    `hirer_user_id`, `equipment_id`, 
    `rental_start_date`, `rental_end_date`, 
    `rental_start_time`, `rental_end_time`, 
    `rental_rate`, `is_perday`, `is_perhour`, 
    `rental_duration`, `rental_delivery_amount`, 
    `rental_delivery_option`, `rental_delivery_address`, 
    `is_active`) VALUES
(1, 1, '2025-10-01', '2025-10-03', NULL, NULL, 150.00, 1, 0, 3, 0.00, 'pickup', NULL, 1),
(2, 3, '2025-10-05', '2025-10-06', NULL, NULL, 500.00, 1, 0, 2, 50.00, 'delivery', '123 Wellington St', 1),
(3, 5, '2025-10-07', NULL, '08:00', '17:00', 20.00, 0, 1, 9, 0.00, 'pickup', NULL, 1),
(4, 7, '2025-10-09', NULL, '09:00', '12:00', 45.00, 0, 1, 3, 15.00, 'delivery', '45 Hamilton Rd', 1),
(5, 9, '2025-10-11', '2025-10-11', NULL, NULL, 60.00, 1, 0, 1, 0.00, 'pickup', NULL, 1),
(6, 11, '2025-10-12', NULL, '08:30', '16:30', 50.00, 0, 1, 8, 10.00, 'delivery', '89 Napier Ave', 1);

-- Transactions

INSERT INTO `equipment_transactions` (
    `request_id`, `payment_mode`, `card_number`, `card_holder_name`, `card_expiration`, `card_cvv`, `transaction_amount`) VALUES
(1, 'credit', '4111111111111111', 'Alice Smith', '12/25', '123', 450.00),
(2, 'debit', '5500000000000004', 'Bob Jones', '11/24', '456', 1000.00),
(3, 'credit', '340000000000009', 'Charlie Ray', '07/26', '789', 180.00),
(4, 'debit', '6011000000000004', 'Diana West', '02/27', '321', 135.00),
(5, 'credit', '4111111111112222', 'Ethan Lee', '05/26', '654', 60.00),
(6, 'debit', '5500000000003333', 'Fiona Chan', '09/27', '987', 400.00);


-- Land
INSERT INTO `land_categories` (`name`) VALUES
('Arable Cropping'),
('Horticulture'),
('Dairy Farming'),
('Dry Stock Farming'),
('Plantation Forestry'),
('Mixed Farming');

INSERT INTO `land_parcels` 
(`name`, `description`, `category_id`, `region_id`, `district_id`, `suburb_id`, `street_name`, `city`, `zip`, `latitude`, `longitude`, `size`, `rate`, `lease_modal`, `file_path`, `user_id`, `is_public`, `is_leased`)
VALUES
('Green Acres Farm', 'Fertile arable cropping land with good irrigation.', 1, 2, 3, 5, 'Country Rd', 'Springfield', '12345', -37.123456, 176.123456, 150, 500, 'per_month', NULL, 2, TRUE, FALSE),
('Sunny Orchards', 'Horticulture land with mature fruit trees.', 2, 2, 4, 7, 'Apple St', 'Orchardville', '54321', -37.654321, 176.654321, 90, 650, 'per_year', NULL, 2, TRUE, TRUE),
('Dairy Meadows', 'Dairy farming land equipped with sheds.', 3, 3, 6, 9, 'Milk Lane', 'Farmtown', '67890', -36.987654, 174.987654, 200, 700, 'per_month', NULL, 2, FALSE, FALSE),
('Hilltop Ranch', 'Dry stock grazing land with good drainage.', 4, 1, 2, 4, 'Ranch Rd', 'Hillville', '56789', -38.123789, 175.456789, 175, 450, 'per_month', NULL, 2, TRUE, FALSE),
('Pinewood Plantations', 'Commercial forestry land ideal for pine plantation.', 5, 3, 7, 11, 'Timber Ave', 'Woodland', '98765', -37.321654, 175.321654, 300, 800, 'per_year', NULL, 3, TRUE, TRUE),
('Valley Mixed Farm', 'Mixed cropping and livestock farming land.', 6, 2, 5, 8, 'Valley View', 'Greenville', '13579', -36.543210, 176.543210, 120, 550, 'per_month', NULL, 3, FALSE, FALSE);


INSERT INTO `land_applications` (`land_parcel_id`, `tenant_id`, `status`)
VALUES
(1, 2, 'pending'),
(3, 2, 'declined'),
(5, 1, 'approved');


INSERT INTO `land_application_details` (`application_id`, `farming_type`, `duration_years`, `experience`, `additional_notes`)
VALUES
(1, 1, 3, '5 years experience in crop farming', 'Interested in expanding irrigation.'),
(2, 3, 5, 'Dairy farming background with herd management experience', 'Looking for long term lease.'),
(3, 5, 2, 'Experience in commercial forestry', 'Plan to invest in new equipment.');


INSERT INTO `land_application_log` (`application_id`, `stage_number`, `stage_name`, `stage_status`, `created_by`, `completed_by`)
VALUES
(1, 1, 'application', 'approved', 2, 5),
(1, 2, 'site_inspection', 'approved', 2, 5),
(1, 3, 'document_verification', 'approved', 2, 5),
(1, 4, 'agreement_signing', 'approved', 2 , 5),

(2, 1, 'application', 'approved', 1, 5),
(2, 2, 'site_inspection', 'approved', 1, 5),
(2, 3, 'document_verification', 'pending', 1, 5);


INSERT INTO `land_site_inspections` (`application_id`, `scheduled_date`, `scheduled_start_time`, `scheduled_end_time`, `inspector_notes`, `created_by`)
VALUES
    (1, '2025-10-15 00:00:00', '09:00', '11:00', 'Initial inspection for soil and drainage.', 2),
    (2, '2025-10-18 00:00:00', '10:00', '12:00', 'Follow-up inspection on drainage issues.', 1),
    (3, '2025-10-20 00:00:00', '08:30', '10:30', 'Check commercial forestry layout.', 3);
    
INSERT INTO `land_document_verification` (`application_id`, `document_type`, `file_path`, `uploaded_by`, `verified_by`) 
VALUES
(1, 'identity', '/uploads/documents/id_proof_1.pdf', 2, 5),
(1, 'finance', '/uploads/documents/financial_statement_1.pdf', 2, NULL),
(2, 'identity', '/uploads/documents/id_proof_2.pdf', 1, 5),
(3, 'reference', '/uploads/documents/forestry_doc_3.pdf', 3, 4);

INSERT INTO `land_agreement` (
  `application_id`, `tenant_id`, `lease_from`, `lease_to`, `rent`, `pricing_modal`, 
  `security_deposit`, `intended_use`, `notes`, `proposed_agreement_doc`, 
  `signed_agreement_doc`, `approved_by`, `created_at`, `updated_at`
) VALUES
(1, 2, '2025-11-01', '2026-11-01', 500.00, 'per_month', 1000.00, 'Arable Cropping', 'Lease for intensive crop farming.', '/docs/proposed/agreement1.pdf', '/docs/signed/agreement1.pdf', 5, NOW(), NOW()),
(2, 2, '2025-12-01', '2027-12-01', 700.00, 'per_month', 1500.00, 'Dairy Farming', 'Long term lease for dairy production.', '/docs/proposed/agreement2.pdf', NULL, 4, NOW(), NOW()),
(3, 1, '2025-10-15', '2026-10-15', 8000.00, 'per_year', 2500.00, 'Plantation Forestry', 'Lease for pine plantation expansion.', '/docs/proposed/agreement3.pdf', '/docs/signed/agreement3.pdf', NULL, NOW(), NOW());
