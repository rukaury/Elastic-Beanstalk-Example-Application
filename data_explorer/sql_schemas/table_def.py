
def get_table_def():
    tables = {}
    tables["comments"] = """
    CREATE TABLE comments(
        course_code VARCHAR(20),
        survey_id VARCHAR(15),
        fiscal_year VARCHAR(9),
        quarter VARCHAR(5),
        learner_classif VARCHAR(80),
        offering_city_en VARCHAR(60),
        original_question VARCHAR(60),
        text_answer TEXT,
        offering_city_fr VARCHAR(60),
        short_question VARCHAR(60),
        text_answer_fr VARCHAR(90),
        overall_satisfaction TINYINT,
        stars TINYINT,
        PRIMARY KEY(survey_id, original_question)
    );
    """
    tables["lsr_last_year"] = """
    CREATE TABLE lsr_last_year(
        course_title_en VARCHAR(200),
        course_title_fr VARCHAR(300),
        course_code VARCHAR(20),
        business_type VARCHAR(30),
        offering_id INT,
        start_date DATE,
        end_date DATE,
        month_en VARCHAR(10),
        month_fr VARCHAR(10),
        client VARCHAR(50),
        offering_status VARCHAR(30),
        offering_language VARCHAR(50),
        offering_region_en VARCHAR(30),
        offering_region_fr VARCHAR(30),
        offering_province_en VARCHAR(30),
        offering_province_fr VARCHAR(30),
        offering_city VARCHAR(50),
        offering_lat FLOAT,
        offering_lng FLOAT,
        learner_province VARCHAR(30),
        learner_city VARCHAR(50),
        learner_lat FLOAT,
        learner_lng FLOAT,
        reg_id INT PRIMARY KEY,
        reg_status VARCHAR(30),
        no_show INT,
        learner_id VARCHAR(22),
        learner_language VARCHAR(10),
        learner_classif VARCHAR(40),
        billing_dept_name_en VARCHAR(150),
        billing_dept_name_fr VARCHAR(200)
    );
    """
    tables['lsr_this_year'] = """
    CREATE TABLE lsr_this_year(
        course_title_en VARCHAR(200),
        course_title_fr VARCHAR(300),
        course_code VARCHAR(20),
        business_type VARCHAR(30),
        offering_id INT,
        start_date DATE,
        end_date DATE,
        month_en VARCHAR(10),
        month_fr VARCHAR(10),
        client VARCHAR(50),
        offering_status VARCHAR(30),
        offering_language VARCHAR(50),
        offering_region_en VARCHAR(30),
        offering_region_fr VARCHAR(30),
        offering_province_en VARCHAR(30),
        offering_province_fr VARCHAR(30),
        offering_city VARCHAR(50),
        offering_lat FLOAT,
        offering_lng FLOAT,
        learner_province VARCHAR(30),
        learner_city VARCHAR(50),
        learner_lat FLOAT,
        learner_lng FLOAT,
        reg_id INT PRIMARY KEY,
        reg_status VARCHAR(30),
        no_show INT,
        learner_id VARCHAR(22),
        learner_language VARCHAR(10),
        learner_classif VARCHAR(40),
        billing_dept_name_en VARCHAR(150),
        billing_dept_name_fr VARCHAR(200)
    );

    """
    tables["product_info"] = """
    CREATE TABLE product_info(
        course_code VARCHAR(20) PRIMARY KEY,
        course_description_en TEXT,
        course_description_fr TEXT, 
        business_type_en VARCHAR(40),
        business_type_fr VARCHAR(40),
        provider_en VARCHAR(30),
        provider_fr VARCHAR(30),
        displayed_on_gccampus_en VARCHAR(5),
        displayed_on_gccampus_fr VARCHAR(5),
        duration FLOAT,
        main_topic_en VARCHAR(50),
        main_topic_fr VARCHAR(50),
        business_line_en VARCHAR(50),
        business_line_fr VARCHAR(50),
        required_training_en VARCHAR(5),
        required_training_fr VARCHAR(5),
        communities_en VARCHAR(110),
        communities_fr VARCHAR(110),
        point_of_contact VARCHAR(80),
        director VARCHAR(40),
        program_manager VARCHAR(40),
        project_lead VARCHAR(40)
    );
    """
    tables["ratings"] = """
    CREATE TABLE ratings(
        course_code VARCHAR(20),
        month VARCHAR(10),
        short_question_en VARCHAR(60),
        short_question_fr VARCHAR(60),
        long_question_en VARCHAR(170),
        long_question_fr VARCHAR(170),
        numerical_answer FLOAT,
        four_or_five SMALLINT,
        count SMALLINT
    );
    """
    return tables
  