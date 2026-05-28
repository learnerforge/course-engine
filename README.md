# Course Discovery Engine

A comprehensive course discovery engine that aggregates, processes, and maps online courses from various providers to technical roles and skills. The engine scrapes, cleans, deduplicates, and enriches course data to create a searchable database of courses with skill extraction and role mapping capabilities.

## Features

- **Multi-source Aggregation**: Collects courses from 30+ providers including NPTEL, Microsoft Learn, MIT OpenCourseWare, freeCodeCamp, and many more
- **Data Processing Pipeline**: 
  - URL cleaning and normalization
  - Category and discipline resolution (especially for NPTEL)
  - Deduplication based on URL and title similarity
  - Skill extraction from course titles and descriptions
  - Role mapping to 25+ technical job roles
- **Quality Scoring**: Assigns data quality scores to each course based on completeness of fields
- **Multiple Output Formats**: Generates CSV, SQLite database, and Excel files for easy consumption
- **Extensive Skill Taxonomy**: Extracts and normalizes skills from a predefined list of 100+ technical skills
- **Role-Based Mapping**: Maps courses to job roles with relevance scores based on skill matching

## Data Sources

The engine currently aggregates courses from the following providers:

### Working Sources (Courses Successfully Ingested)
- **NPTEL**: 3,353 courses (Indian Institute of Technology courses)
- **Microsoft Learn**: 4,738 courses (Microsoft's learning platform)
- **MIT OpenCourseWare**: 2,574 courses (MIT's free course materials)
- **freeCodeCamp**: 8,979 courses (Open-source coding curriculum)
- **Docker Docs**: 1,658 courses (Docker documentation tutorials)
- **Hyperskill**: 457 courses (JetBrains Academy)
- **Exercism**: 82 courses (Programming practice platform)
- **Google Codelabs**: 219 courses (Google's hands-on coding tutorials)
- **Oracle Learning Explorer**: 985 courses (Oracle's free learning platform)
- **Odin Project**: 3 courses (Full-stack web development curriculum)
- **Cisco Networking Academy**: 71 courses (Networking education)
- **CognitiveClass (IBM)**: 652 courses (IBM's data science and AI courses)
- **Codecademy**: 956 courses (Interactive coding platform)
- **Educative**: 177 courses (Text-based interactive learning)
- **DeepLearning.AI**: 135 courses (Andrew Ng's AI courses)
- **Frontend Masters**: 471 courses (Frontend web development)
- **Atlassian University**: 16 courses (Atlassian tools training)
- **Next.js Learn**: 112 courses (React framework tutorials)
- **Flutter Learn**: 19 courses (Google's UI toolkit)
- **Laravel Learn**: 25 courses (PHP framework tutorials)
- **Stepik**: 14,669 courses (Russian educational platform)
- **KodeKloud**: 21 courses (DevOps and cloud engineering)

### Processing Statistics (After Latest Run)
- **Total Courses**: 40,118 (after deduplication)
- **Total Skills Extracted**: 89,712
- **Total Role Mappings**: 84,420
- **Technical Roles Covered**: 25 (including Frontend Developer, Backend Developer, Data Scientist, DevOps Engineer, etc.)

## Output Files

The engine generates the following files in the `data/exports/` directory:

1. **`1_providers.csv`**: Metadata about each course provider
2. **`2_courses.csv`**: Main course catalog with detailed course information
3. **`3_course_skills.csv`**: Extracted skills mapped to each course
4. **`4_roles.csv`**: Technical role definitions with required/optional skills
5. **`5_role_course_mapping.csv`**: Mapping of courses to roles with relevance scores
6. **`6_scrape_runs.csv`**: Statistics from each scraping run
7. **`7_validation_report.csv`**: Data quality validation report

Additionally, the engine creates:
- **SQLite Database**: `data/database/course_engine.sqlite` containing all data in relational tables
- **Excel Workbook**: `data/exports/courses_dataset.xlsx` with all data in separate sheets

## Course Data Schema

Each course record includes:
- Basic Information: ID, title, description, URL, provider
- Categorization: Category, subcategory, difficulty level
- Metadata: Duration, language, price, certificate availability
- Skills: Extracted technical skills with confidence scores
- Quality Metrics: Data quality score (0-100)
- Relationships: Role mappings with relevance scores

## Skill Extraction

The engine extracts skills from course titles and descriptions using a comprehensive taxonomy of:
- Programming Languages (Python, JavaScript, Java, C#, etc.)
- Frameworks & Libraries (React, Django, TensorFlow, etc.)
- Cloud Platforms (AWS, Azure, Google Cloud)
- Databases (SQL, PostgreSQL, MongoDB, etc.)
- DevOps Tools (Docker, Kubernetes, Jenkins, etc.)
- Data Science & ML (Pandas, Scikit-learn, PyTorch, etc.)
- Web Technologies (HTML, CSS, GraphQL, etc.)
- And many more technical domains

## Role Mapping

Courses are mapped to 25 technical roles including:
- Frontend/Backend/Full Stack Developer
- Data Scientist/Analyst/Engineer
- Machine Learning/AI Engineer
- DevOps/Cloud/Security Engineer
- Mobile App Developer
- UI/UX Designer
- Database Administrator
- And more specialized roles

Each mapping includes a relevance score (0-100) based on:
- Skill matching (required vs optional skills)
- Title and category relevance
- Provider trust score
- Credential value (certificates/badges)

## Installation & Usage

Since this is a data processing engine rather than a deployable application, usage involves:

1. **Running the Pipeline**:
   ```bash
   python _fix_and_rebuild.py
   ```
   This will:
   - Fix known issues in raw data (NPTEL categories, MS Learn URL tracking parameters)
   - Re-normalize all course data
   - Re-extract skills and re-generate role mappings
   - Produce all output files

2. **Accessing the Data**:
   - Directly query the SQLite database: `data/database/course_engine.sqlite`
   - Use the CSV files for import into other systems
   - Open the Excel workbook for filtered viewing and analysis

3. **Customizing Sources**:
   - Modify `sources_registry.yml` to add/remove sources or change their status
   - The pipeline respects the status flags (working, experimental, blocked, etc.)

## Data Quality & Validation

The engine implements multiple quality checks:
- **URL Validation**: Removes tracking parameters and verifies accessibility
- **Deduplication**: Removes duplicate courses based on URL similarity
- **Quality Scoring**: Each course receives a score based on completeness of fields
- **Validation Reports**: Generated per provider showing completeness metrics
- **Error Logging**: Detailed logs in `logs/scraper.log` and `logs/url_validation_*.txt`

## Future Enhancements

Planned improvements for the course discovery engine:
- Web interface for course search and filtering
- API endpoint for programmatic access
- Integration with additional providers (Coursera, Udemy, edX via APIs)
- Enhanced skill extraction using NLP techniques
- Course similarity detection and recommendation engine
- User preference learning for personalized course recommendations
- Integration with learning management systems

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Thanks to all the course providers who make their educational content freely available, enabling platforms like this course discovery engine to help learners find relevant educational resources.

Last updated: May 28, 2026