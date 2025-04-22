import os
import time
import random
from typing import Dict, List, Optional
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
import logging
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ActionNetworkScraper:
    def __init__(self):
        """Initialize the Action Network scraper with login credentials."""
        load_dotenv()
        self.email = os.getenv('ACTION_NETWORK_EMAIL')
        self.password = os.getenv('ACTION_NETWORK_PASSWORD')
        self.base_url = "https://www.actionnetwork.com"
        
        if not self.email or not self.password:
            raise ValueError("Please set ACTION_NETWORK_EMAIL and ACTION_NETWORK_PASSWORD in .env file")
        
        try:
            # Set up Chrome options
            options = webdriver.ChromeOptions()
            
            # Add anti-detection measures
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--start-maximized')
            
            # Add realistic user agent
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
            
            # Add experimental options
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Initialize ChromeDriver with service
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Add CDP commands to avoid detection
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
            
            # Set longer page load timeout
            self.driver.set_page_load_timeout(30)
            
            # Initialize wait with longer timeout
            self.wait = WebDriverWait(self.driver, 20)
            
            logger.info("ChromeDriver initialized successfully with anti-detection measures")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromeDriver: {str(e)}")
            raise

    def random_delay(self):
        """Add a random delay between actions."""
        delay = random.uniform(0.1, 0.3)
        time.sleep(delay)

    def add_random_mouse_movements(self):
        """Simulate random mouse movements."""
        try:
            actions = ActionChains(self.driver)
            for _ in range(random.randint(2, 5)):
                x = random.randint(0, 500)
                y = random.randint(0, 500)
                actions.move_by_offset(x, y)
                actions.perform()
                time.sleep(random.uniform(0.1, 0.3))
        except:
            pass

    def verify_login(self, timeout=25):
        """Verify successful login by checking multiple indicators."""
        try:
            logging.info("Starting login verification...")
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                # Check if we're still on the login page
                if "/login" in self.driver.current_url:
                    time.sleep(0.5)
                    continue
                    
                # If we're redirected away from login, consider it successful
                if "/login" not in self.driver.current_url:
                    logging.info("Login verified - redirected from login page")
                    return True
                    
            logging.error(f"Login verification timed out after {timeout} seconds")
            return False
            
        except Exception as e:
            logging.error(f"Error during login verification: {str(e)}")
            return False

    def navigate_to_mlb_pro_report(self):
        """Navigate to the MLB Sharp Report page."""
        try:
            logging.info("Navigating to MLB Sharp Report...")
            
            # Navigate directly to the Sharp Report page
            self.driver.get("https://www.actionnetwork.com/mlb/sharp-report")
            
            # Wait longer for the page to load
            time.sleep(10)
            
            # Wait for the date navigation to be present
            logger.info("Waiting for date navigation to load...")
            try:
                # Wait for the date container with exact class
                date_container = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "odds-tools-sub-nav__date"))
                )
                
                # Wait for the date display
                date_display = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "day-nav__display"))
                )
                
                logger.info(f"Found date display showing: {date_display.text}")
                return True
                
            except Exception as e:
                logger.error(f"Error waiting for page elements: {str(e)}")
                self.driver.save_screenshot("page_load_error.png")
                return False
            
        except Exception as e:
            logger.error(f"Error navigating to MLB Sharp Report: {str(e)}")
            try:
                self.driver.save_screenshot("navigation_error.png")
            except:
                pass
            return False

    def login(self):
        """Log in to Action Network with enhanced anti-detection."""
        try:
            logging.info("Starting enhanced login process...")
            
            # Clear cookies and cache first
            self.driver.delete_all_cookies()
            
            # Navigate to home page first
            self.driver.get(self.base_url)
            time.sleep(2)  # Wait for home page to load
            
            # Then navigate to login page
            self.driver.get(f"{self.base_url}/login")
            logging.info("Navigated to login page")
            
            # Wait for email field with increased timeout
            email_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
            )
            
            # Type email like a human
            for char in self.email:
                email_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            logging.info("Email entered successfully")
            
            # Small pause before password
            time.sleep(random.uniform(0.5, 1.0))
            
            # Find and fill password field
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            for char in self.password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            logging.info("Password entered successfully")
            
            # Small pause before clicking login
            time.sleep(random.uniform(0.5, 1.0))
            
            # Find and click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            # Move mouse to button naturally
            action = ActionChains(self.driver)
            action.move_to_element(login_button)
            action.pause(random.uniform(0.1, 0.3))
            action.click()
            action.perform()
            
            logging.info("Clicked login button")
            
            # Wait longer for login verification
            if not self.verify_login(timeout=25):
                logging.error("Login verification failed")
                self.driver.save_screenshot("login_failed.png")
                return False
            
            # Additional wait after successful login
            time.sleep(3)
            
            logging.info("Login successful")
            return True
            
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            self.driver.save_screenshot("login_error.png")
            return False

    def select_date(self, target_date: datetime) -> bool:
        """Navigate to the target date using the date navigation arrows."""
        try:
            logger.info(f"Starting date navigation to target date: {target_date.strftime('%m/%d/%Y')}")
            
            # Wait for the date navigation container with exact class
            date_container = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.odds-tools-sub-nav__date"))
            )
            
            # Find the Previous Date button using exact classes and aria-label
            left_arrow = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "button.day-nav__button[aria-label='Previous Date']"))
            )
            
            # Find the date display
            date_display = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "day-nav__display"))
            )
            
            # Click the left arrow until we reach the target date
            max_clicks = 30
            clicks = 0
            
            while clicks < max_clicks:
                # Get current date text
                current_date_text = date_display.text.strip()  # Format: "Fri Mar 28"
                try:
                    current_date = datetime.strptime(current_date_text, "%a %b %d")
                    current_date = current_date.replace(year=target_date.year)
                    logger.info(f"Current date: {current_date.strftime('%m/%d/%Y')}")
                    
                    if current_date.date() <= target_date.date():
                        logger.info("Reached target date")
                        break
                    
                    # Make sure the button is clickable
                    left_arrow = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 
                            "button.day-nav__button[aria-label='Previous Date']"))
                    )
                    
                    # Click using JavaScript
                    self.driver.execute_script("arguments[0].click();", left_arrow)
                    logger.info("Clicked left arrow")
                    
                    # Wait for date to update
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error during date navigation: {str(e)}")
                    return False
                
                clicks += 1
            
            if clicks >= max_clicks:
                logger.error("Reached maximum number of clicks without finding target date")
                return False
            
            # Final verification
            final_date_text = date_display.text.strip()
            final_date = datetime.strptime(final_date_text, "%a %b %d")
            final_date = final_date.replace(year=target_date.year)
            
            if final_date.date() <= target_date.date():
                logger.info(f"Successfully navigated to date: {final_date.strftime('%m/%d/%Y')}")
                time.sleep(2)  # Wait for content to load
                return True
            else:
                logger.error(f"Failed to reach target date. Current: {final_date.strftime('%m/%d/%Y')}, Target: {target_date.strftime('%m/%d/%Y')}")
                return False
            
        except Exception as e:
            logger.error(f"Error in date selection: {str(e)}")
            self.driver.save_screenshot("date_selection_error.png")
            return False

    def _check_signal(self, container, signal_class: str) -> str:
        """Check if a signal is active (blue) by checking for the specific css class."""
        try:
            # Try multiple selectors to find the signal
            selectors = [
                f"button[class*='{signal_class}']",  # Direct button with signal class
                f"div[class*='{signal_class}']",     # Div with signal class
                f"[class*='{signal_class}']"         # Any element with signal class
            ]
            
            for selector in selectors:
                try:
                    signal = container.find_element(By.CSS_SELECTOR, selector)
                    # Get both class and style attributes
                    class_name = signal.get_attribute('class') or ''
                    style = signal.get_attribute('style') or ''
                    background_color = signal.value_of_css_property('background-color')
                    computed_style = self.driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).getPropertyValue('background-color');",
                        signal
                    )
                    
                    # Log what we found for debugging
                    logger.info(f"Signal {signal_class} - Class: {class_name}")
                    logger.info(f"Signal {signal_class} - Style: {style}")
                    logger.info(f"Signal {signal_class} - Background: {background_color}")
                    logger.info(f"Signal {signal_class} - Computed Style: {computed_style}")
                    
                    # Take screenshot of the signal for verification
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", signal)
                    time.sleep(0.5)  # Wait for scroll
                    signal.screenshot(f"signal_{signal_class}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                    
                    # Check for blue indicators:
                    # 1. Specific class
                    # 2. Background color
                    # 3. Style attribute
                    # 4. Computed style
                    if ('css-1m5q1hm' in class_name or 
                        'active' in class_name.lower() or
                        'rgb(0, 121, 240)' in background_color or
                        '#0079F0' in style or
                        'rgb(0, 121, 240)' in style or
                        'rgb(0, 121, 240)' in computed_style):
                        logger.info(f"Found active {signal_class} signal")
                        return 'X'
                except Exception as e:
                    logger.warning(f"Failed to check selector {selector}: {str(e)}")
                    continue
            
            return ''
        except Exception as e:
            logger.error(f"Error checking signal {signal_class}: {str(e)}")
            return ''

    def scrape_date(self, target_date: datetime) -> pd.DataFrame:
        """Scrape the Sharp Report data for a specific date and return as a DataFrame."""
        try:
            # Select the target date
            if not self.select_date(target_date):
                logger.error("Failed to select date")
                return pd.DataFrame()
            
            # Take one screenshot of the page after date selection
            self.driver.save_screenshot(f"page_after_date_selection_{target_date.strftime('%Y%m%d')}.png")
            
            # Wait for game rows to be present with more precise selectors
            logger.info("Waiting for game data to load...")
            try:
                # Wait longer for the page to load
                time.sleep(5)
                
                # Try more precise selectors for game rows
                game_row_selectors = [
                    "div[class*='GameRow']",  # Most specific
                    "div[class*='game-row']",
                    "div[class*='Game']",
                    "div[class*='game']"
                ]
                
                game_rows = None
                for selector in game_row_selectors:
                    try:
                        # Only look for visible elements
                        game_rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        # Filter to only visible rows
                        game_rows = [row for row in game_rows if row.is_displayed()]
                        if game_rows:
                            logger.info(f"Found {len(game_rows)} game rows using selector: {selector}")
                            break
                    except:
                        continue
                
                if not game_rows:
                    logger.info(f"No games available for {target_date.strftime('%m/%d/%Y')}")
                    return pd.DataFrame()
                
                # Take one screenshot of all games
                self.driver.save_screenshot(f"games_{target_date.strftime('%Y%m%d')}.png")
                
            except TimeoutException:
                logger.error("Timeout waiting for game rows to appear")
                return pd.DataFrame()

            # Prepare data for DataFrame
            data = []
            
            for idx, row in enumerate(game_rows, 1):
                try:
                    logger.info(f"Processing game {idx} of {len(game_rows)}")
                    
                    # Extract team names with more precise selectors
                    team_selectors = [
                        "div[class*='TeamName']",  # Most specific
                        "div[class*='team-name']",
                        "div[class*='Team']",
                        "div[class*='team']"
                    ]
                    
                    team_elements = None
                    for selector in team_selectors:
                        try:
                            team_elements = row.find_elements(By.CSS_SELECTOR, selector)
                            # Filter to only visible elements
                            team_elements = [el for el in team_elements if el.is_displayed()]
                            if len(team_elements) == 2:
                                break
                        except:
                            continue
                    
                    if not team_elements or len(team_elements) != 2:
                        logger.warning(f"Skipping game {idx} - could not find both team names")
                        continue
                        
                    away_team = team_elements[0].text.strip()
                    home_team = team_elements[1].text.strip()
                    
                    logger.info(f"Processing game: {away_team} @ {home_team}")
                    
                    # Try more precise selectors for the signals container
                    signals_container = None
                    container_selectors = [
                        "div[class*='sharp-report__signal-buttons-container']",  # Most specific
                        "div[class*='ProReportSignals']",
                        "div[class*='SignalButtons']",
                        "div[class*='Signals']"
                    ]
                    
                    for selector in container_selectors:
                        try:
                            signals_container = row.find_element(By.CSS_SELECTOR, selector)
                            if signals_container.is_displayed():
                                logger.info(f"Found signals container with selector: {selector}")
                                break
                        except:
                            continue
                    
                    if not signals_container:
                        logger.error("Could not find signals container")
                        continue
                    
                    # Check each signal type
                    signals = {
                        'Sharp Action': self._check_signal(signals_container, 'SharpAction'),
                        'Big Money': self._check_signal(signals_container, 'BigMoney'),
                        'Systems': self._check_signal(signals_container, 'Systems'),
                        'Projections': self._check_signal(signals_container, 'Projections'),
                        'Top Experts': self._check_signal(signals_container, 'ExpertPicks')
                    }
                    
                    # Log found signals
                    active_signals = [k for k, v in signals.items() if v == 'X']
                    if active_signals:
                        logger.info(f"Found active signals: {', '.join(active_signals)}")
                    
                    # Extract spread and price with more precise selectors
                    spread = ''
                    price = ''
                    
                    spread_selectors = ["div[class*='Spread']", "div[class*='spread']"]
                    price_selectors = ["div[class*='Price']", "div[class*='price']"]
                    
                    for selector in spread_selectors:
                        try:
                            spread_element = row.find_element(By.CSS_SELECTOR, selector)
                            if spread_element.is_displayed():
                                spread = spread_element.text.strip()
                                break
                        except:
                            continue
                            
                    for selector in price_selectors:
                        try:
                            price_element = row.find_element(By.CSS_SELECTOR, selector)
                            if price_element.is_displayed():
                                price = price_element.text.strip()
                                break
                        except:
                            continue
                    
                    logger.debug(f"Spread: {spread}, Price: {price}")
                    
                    # Create row for away team
                    away_data = {
                        'Date': target_date.strftime('%m/%d/%Y'),
                        'Home / Away': 'Away',
                        'Team': away_team,
                        **signals,
                        'SPREAD (+/-1.5)': spread,
                        'PRICE': price,
                        'Result': ''
                    }
                    data.append(away_data)
                    
                    # Create row for home team with adjusted spread
                    home_data = away_data.copy()
                    home_data.update({
                        'Home / Away': 'Home',
                        'Team': home_team,
                        'SPREAD (+/-1.5)': str(-float(spread.strip('-'))) if spread else ''
                    })
                    data.append(home_data)
                    
                except Exception as e:
                    logger.error(f"Error processing game row {idx}: {str(e)}")
                    continue
            
            if not data:
                logger.warning(f"No game data was found for date {target_date.strftime('%m/%d/%Y')}")
                return pd.DataFrame()
                
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Reorder columns to match template
            columns = [
                'Date', 'Home / Away', 'Team', 'Big Money', 'Sharp Action',
                'Systems', 'Projections', 'Top Experts', 'SPREAD (+/-1.5)',
                'PRICE', 'Result'
            ]
            df = df[columns]
            
            logger.info(f"Successfully scraped data for {len(df) // 2} games on {target_date.strftime('%m/%d/%Y')}")
            return df
            
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            logger.error("Stack trace:", exc_info=True)
            return pd.DataFrame()

    def scrape_date_range(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Scrape data for a range of dates."""
        all_data = []
        current_date = start_date
        
        while current_date <= end_date:
            logger.info(f"Scraping data for {current_date.strftime('%m/%d/%Y')}")
            df = self.scrape_date(current_date)
            if not df.empty:
                all_data.append(df)
            current_date += timedelta(days=1)
            time.sleep(2)  # Add delay between dates
            
        if not all_data:
            return pd.DataFrame()
            
        return pd.concat(all_data, ignore_index=True)

    def save_to_excel(self, df: pd.DataFrame, filename: str = None) -> bool:
        """Save the scraped data to an Excel file."""
        try:
            if df.empty:
                logger.error("No data to save")
                return False

            # Create data directory if it doesn't exist
            data_dir = os.path.join(os.getcwd(), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            # Generate filename if not provided
            if not filename:
                filename = f"mlb_signals_{datetime.now().strftime('%Y%m%d')}.xlsx"
            
            # Full path for the Excel file
            filepath = os.path.join(data_dir, filename)
            
            # Save to Excel with formatting
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='MLB Signals')
                
                # Get the worksheet
                worksheet = writer.sheets['MLB Signals']
                
                # Format headers
                for col in range(1, len(df.columns) + 1):
                    cell = worksheet.cell(row=1, column=col)
                    cell.font = openpyxl.styles.Font(bold=True)
                    
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            
            logger.info(f"Data saved to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to Excel: {str(e)}")
            return False

    def run(self, start_date: datetime = None, end_date: datetime = None, output_file: str = None) -> bool:
        """Run the scraper for a date range and save the results to Excel."""
        try:
            if not self.login():
                return False
                
            # Navigate to MLB Pro Report after successful login
            if not self.navigate_to_mlb_pro_report():
                return False
                
            logger.info("Starting to scrape data...")
            
            # Focus on March 27th, 2024
            target_date = datetime(2024, 3, 27)
            df = self.scrape_date(target_date)
            
            if not df.empty:
                # Generate output filename if not provided
                if not output_file:
                    output_file = f"mlb_signals_{target_date.strftime('%Y%m%d')}.xlsx"
                    
                success = self.save_to_excel(df, output_file)
                logger.info("Scraping completed successfully")
                return success
            return False
            
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            return False
        finally:
            self.driver.quit()

if __name__ == "__main__":
    # Set up date range from March 27th to present
    start_date = datetime(2024, 3, 27)
    end_date = datetime.now()
    
    try:
        scraper = ActionNetworkScraper()
        output_file = f"mlb_signals_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.xlsx"
        success = scraper.run(start_date=start_date, end_date=end_date, output_file=output_file)
        
        if not success:
            logger.error("Scraper failed to complete successfully")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Scraper failed with error: {str(e)}")
        sys.exit(1) 