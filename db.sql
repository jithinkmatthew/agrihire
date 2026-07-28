DROP database IF EXISTS `agrihire`;

CREATE SCHEMA `agrihire`;
USE `agrihire`;

-- Location Regions
CREATE TABLE location_regions(
	`region_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
	`name` VARCHAR(100)
);

-- Location Districts
CREATE TABLE location_districts(
	`district_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(100),
	`region_id` INT NOT NULL,
	CONSTRAINT fk_region_id
		FOREIGN KEY (region_id) REFERENCES location_regions(region_id) 
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

-- Location Suburbs
CREATE TABLE location_suburbs(
	`suburb_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(100),
	`district_id` INT NOT NULL,
	CONSTRAINT fk_district_id
		FOREIGN KEY (district_id) REFERENCES location_districts(district_id) 
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

-- Location Street
-- CREATE TABLE location_street_details(
--     `street_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
--     `street_name` VARCHAR(255),
--     `city` VARCHAR(255),
--     `zip` VARCHAR(255),
--     `suburb_id` INT NOT NULL,
--     CONSTRAINT fk_suburb_id
--         FOREIGN KEY (suburb_id) REFERENCES location_suburbs(suburb_id) 
--         ON DELETE CASCADE
--         ON UPDATE CASCADE
-- );

-- Users
CREATE TABLE users (
	`user_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`username` VARCHAR(20) NOT NULL,
	`first_name` VARCHAR(20),
	`last_name` VARCHAR(20),
	`email` VARCHAR(255) NOT NULL,
	`mobile` VARCHAR(20),
	`location` VARCHAR(255),
	`password_hash` CHAR(60) NOT NULL,
	`profile_image` VARCHAR(255),
	-- `suburb_id` INT,
	-- CONSTRAINT fk_user_suburb_id
	-- 	FOREIGN KEY (suburb_id) REFERENCES location_suburbs(suburb_id) 
	-- 	ON DELETE CASCADE
	-- 	ON UPDATE CASCADE,
	UNIQUE KEY `username` (`username`),
	UNIQUE KEY `email` (`email`)
);

-- Equipment Categories
CREATE TABLE equipment_categories (
    `category_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Equipment SubCategories
CREATE TABLE equipment_subcategories (
    `subcategory_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `category_id` INT,
    `name` VARCHAR(100) NOT NULL,
    CONSTRAINT fk_category
        FOREIGN KEY (category_id) REFERENCES equipment_categories(category_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Equipment table
CREATE TABLE equipments (
    `equipment_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `make` VARCHAR(255),
    `model` VARCHAR(255),
    `year` YEAR,
    `category_id` INT,
    `sub_category_id` INT,
    `user_id` INT,
    `description` TEXT,
    `price` INT,
    `price_modal` VARCHAR(10),
    `region_id` INT,
    `district_id` INT,
    `suburb_id` INT,
    `street_name` VARCHAR(255),
    `city` VARCHAR(255),
    `zip` VARCHAR(20),
    `latitude` DECIMAL(10, 8),
    `longitude` DECIMAL(11, 8),
    `height` INT UNSIGNED,
    `length` INT UNSIGNED,
    `width` INT UNSIGNED,
    `weight` INT UNSIGNED NULL,
    `is_public` BOOLEAN NOT NULL,
    `is_hired` BOOLEAN NOT NULL,
    `status` ENUM('listed', 'payment_completed', 'ready_for_pickup', 'in_use', 'returned') NOT NULL DEFAULT 'listed',
	`created_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_date` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT fk_eqp_category
        FOREIGN KEY (category_id) REFERENCES equipment_categories(category_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT fk_eqp_sub_category
        FOREIGN KEY (sub_category_id) REFERENCES equipment_subcategories(subcategory_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_eqp_user_id
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT fk_region
        FOREIGN KEY (region_id) REFERENCES location_regions(region_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT fk_district
        FOREIGN KEY (district_id) REFERENCES location_districts(district_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT fk_suburb
        FOREIGN KEY (suburb_id) REFERENCES location_suburbs(suburb_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE    
);

CREATE INDEX idx_equipment_location ON equipments(region_id, district_id, suburb_id);
CREATE INDEX idx_equipment_category ON equipments(category_id, sub_category_id);

-- Safety options
CREATE TABLE safety_options (
    `safety_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL
);

-- Junction table to link equipment with multiple safety options
CREATE TABLE equipment_safety_options (
    `equipment_id` INT NOT NULL,
    `safety_id` INT NOT NULL,
    `assigned_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (equipment_id, safety_id),
	CONSTRAINT fk_equipment_id
        FOREIGN KEY (equipment_id) REFERENCES equipments(equipment_id) 
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CONSTRAINT fk_safety_id
        FOREIGN KEY (safety_id) REFERENCES safety_options(safety_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE equipment_files (
    `file_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `equipment_id` INT NOT NULL,
    `file_path` VARCHAR(255) NOT NULL,
    `file_type` ENUM('image', 'safety_doc') NOT NULL,
    `user_id` INT,
    `uploaded_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_eqp_files_equipment_id
        FOREIGN KEY (equipment_id) REFERENCES equipments(equipment_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
    CONSTRAINT fk_eqp_files_user_id
        FOREIGN KEY (user_id) REFERENCES users(user_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE equipment_requests (
    `request_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `hirer_user_id` INT NOT NULL,
    `equipment_id` INT NOT NULL,
    `rental_start_date` DATE,
    `rental_end_date` DATE,
    `rental_start_time` VARCHAR(10),
    `rental_end_time` VARCHAR(10),
    `rental_rate` DECIMAL(10,2) NOT NULL,
    `is_perday` BOOLEAN,
    `is_perhour` BOOLEAN,
    `rental_duration` DECIMAL(10,1),
    `rental_delivery_amount` DECIMAL(10,2),
    `rental_delivery_option` VARCHAR(10) NOT NULL,
    `rental_delivery_address` VARCHAR(80),
    -- `status` ENUM('pending_payment', 'payment_complete', 'ready_for_pickup', 'in_use', 'returned') NOT NULL DEFAULT 'pending_payment',
    `is_active` BOOLEAN,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_hirer_user_id FOREIGN KEY (hirer_user_id) 
        REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,    
    
    CONSTRAINT fk_request_equipment FOREIGN KEY (equipment_id) 
        REFERENCES equipments(equipment_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE

);

CREATE TABLE equipment_transactions (
    `transaction_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `request_id` INT NOT NULL,
    `payment_mode` VARCHAR(10) NOT NULL,
    `card_number` VARCHAR(20),
    `card_holder_name` VARCHAR(100),
    `card_expiration` VARCHAR(7),
    `card_cvv` VARCHAR(4),
    `transaction_amount` DECIMAL(10,2),
    CONSTRAINT fk_transaction_request FOREIGN KEY (request_id) 
        REFERENCES equipment_requests(request_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- LAND --

CREATE TABLE land_categories (
    `category_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE land_parcels (
    `land_parcel_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `category_id` INT,
    `region_id` INT,
    `district_id` INT,
    `suburb_id` INT,
    `street_name` VARCHAR(255),
    `city` VARCHAR(255),
    `zip` VARCHAR(20),
    `latitude` DECIMAL(10, 8),
    `longitude` DECIMAL(11, 8),
    `size` INT UNSIGNED,
    `rate` INT,
    `lease_modal` VARCHAR(10),
    `file_path` VARCHAR(255),
    `user_id` INT,
    `is_public` BOOLEAN NOT NULL,
    `is_leased` BOOLEAN NOT NULL,
    -- `status` ENUM('listed', 'payment_completed', 'ready_for_pickup', 'in_use', 'returned') NOT NULL DEFAULT 'listed',
	`created_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_date` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

	CONSTRAINT fk_land_category
        FOREIGN KEY (category_id) REFERENCES land_categories(category_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_land_user_id
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT fk_land_region
        FOREIGN KEY (region_id) REFERENCES location_regions(region_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT fk_land_district
        FOREIGN KEY (district_id) REFERENCES location_districts(district_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT fk_land_suburb
        FOREIGN KEY (suburb_id) REFERENCES location_suburbs(suburb_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE    
);

CREATE INDEX idx_land_location ON land_parcels(region_id, district_id, suburb_id);
CREATE INDEX idx_landcategory ON land_parcels(category_id);

CREATE TABLE land_applications (
    `application_id` INT AUTO_INCREMENT PRIMARY KEY,
    `land_parcel_id` INT NOT NULL,
    `tenant_id` INT NOT NULL,
    `status` ENUM('pending','approved','declined') DEFAULT 'pending',
    -- `current_stage` INT DEFAULT 1,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_land_application_parcel_id
        FOREIGN KEY (land_parcel_id) REFERENCES land_parcels(land_parcel_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_land_application_tenant_id
        FOREIGN KEY (tenant_id) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE land_application_details (
    `application_id` INT PRIMARY KEY,
    `farming_type` INT,
    `duration_years` INT,
    `experience` TEXT,
    `additional_notes` TEXT,

    CONSTRAINT fk_land_application_details_application_id
        FOREIGN KEY (application_id) REFERENCES land_applications(application_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_land_application_details_farming_type
        FOREIGN KEY (farming_type) REFERENCES land_categories(category_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE land_application_log (
    `log_id` INT AUTO_INCREMENT PRIMARY KEY,
    `application_id` INT,
    `stage_number` INT,
    `stage_name` ENUM('application', 'site_inspection', 'document_verification', 'agreement_signing' ),
    `stage_status` ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    `created_by` INT,
    `completed_by` INT NULL,
    `completed_at` DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_land_application_log_appid
        FOREIGN KEY (application_id) REFERENCES land_applications(application_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_land_application_log_created_by
        FOREIGN KEY (created_by) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_land_application_log_completed_by
        FOREIGN KEY (completed_by) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE land_site_inspections (
    `inspection_id` INT AUTO_INCREMENT PRIMARY KEY,
    `application_id` INT NOT NULL,
    `scheduled_date` DATETIME NOT NULL,
    `scheduled_start_time` VARCHAR(10),
    `scheduled_end_time` VARCHAR(10),
    `inspector_notes` TEXT,
    `created_by` INT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_site_insp_application
        FOREIGN KEY (application_id) REFERENCES land_applications(application_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_site_insp_created_by
        FOREIGN KEY (created_by) REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE land_document_verification (
    `document_id` INT AUTO_INCREMENT PRIMARY KEY,
    `application_id` INT NOT NULL,
    `document_type` ENUM('identity', 'finance', 'reference') NOT NULL,
    `file_path` VARCHAR(255) NOT NULL,
    `uploaded_by` INT NOT NULL,
    `verified_by` INT NULL,
    `uploaded_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `verified_at` DATETIME NULL,
    CONSTRAINT fk_document_verification_application
        FOREIGN KEY (application_id) REFERENCES land_applications(application_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_document_verification_uploadedby
        FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,  

    CONSTRAINT fk_document_verification_verifiedby
        FOREIGN KEY (verified_by) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE land_agreement (
    `agreement_id` INT AUTO_INCREMENT PRIMARY KEY,
    `application_id` INT NOT NULL,
    `tenant_id` INT NULL,
    `lease_from` DATE NOT NULL,
    `lease_to` DATE NOT NULL,
    `rent` DECIMAL(10,2) NOT NULL,
    `pricing_modal` ENUM('per_month', 'per_year') NOT NULL,
    `security_deposit` DECIMAL(10,2) NOT NULL,
    `intended_use` VARCHAR(50) NOT NULL,
    `notes` VARCHAR(255) NULL,
    `proposed_agreement_doc` VARCHAR(255) NULL,
    `signed_agreement_doc` VARCHAR(255) NULL,
    `approved_by` INT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_land_agreement_application
        FOREIGN KEY (application_id) REFERENCES land_applications(application_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_land_agreement_tenant
        FOREIGN KEY (tenant_id) REFERENCES users(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_land_agreement_approved_by
        FOREIGN KEY (approved_by) REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);




