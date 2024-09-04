from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

# Configure your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Available options for the select boxes
GENDER_OPTIONS = ["Male", "Female", "Non-binary", "Other"]
AGE_OPTIONS = ["Child", "Teen", "Adult", "Elderly"]
SKIN_TONE_OPTIONS = ["Fair", "Light", "Medium", "Olive", "Brown", "Dark"]
HAIR_COLOR_OPTIONS = ["Black", "Brown", "Blonde", "Red", "Gray", "White"]
HAIR_STYLE_OPTIONS = ["Straight", "Wavy", "Curly", "Bald", "Short", "Long"]
EYE_COLOR_OPTIONS = ["Blue", "Green", "Brown", "Hazel", "Gray", "Amber"]
EYE_SHAPE_OPTIONS = ["Round", "Almond", "Hooded", "Upturned", "Downturned"]
FACIAL_FEATURES_OPTIONS = ["Freckles", "Dimples", "Scar", "Wrinkles"]
EYEBROWS_OPTIONS = ["Thick", "Thin", "Arched", "Straight", "Bushy"]
NOSE_OPTIONS = ["Small", "Large", "Pointed", "Flat", "Wide"]
MOUTH_OPTIONS = ["Full", "Thin", "Wide", "Small"]
CLOTHING_STYLE_OPTIONS = ["Casual", "Formal", "Sporty", "Traditional", "Modern"]
PERSONALITY_TRAITS_OPTIONS = ["Brave", "Clever", "Kind", "Curious", "Funny", "Serious"]
PET_COMPANION_OPTIONS = ["Dog", "Cat", "Bird", "None"]

THEME_OPTIONS = ["Adventure", "Sports", "Safety", "Magic", "Fairytale", "Education", 
                 "Friendship", "Family", "Mystery", "Holidays & Celebrations", 
                 "Nature & Environment", "Special Needs Awareness", 
                 "Careers & Aspirations", "Travel & Exploration"]

FORMAT_OPTIONS = ["Physical Book", "Audiobook", "Ebook", "Animated Cartoon", 
                  "Personalised Storybook", "Nursery Rhymes"]

@app.route('/')
def index():
    return render_template('index.html', 
                           gender_options=GENDER_OPTIONS, 
                           age_options=AGE_OPTIONS,
                           skin_tone_options=SKIN_TONE_OPTIONS,
                           hair_color_options=HAIR_COLOR_OPTIONS,
                           hair_style_options=HAIR_STYLE_OPTIONS,
                           eye_color_options=EYE_COLOR_OPTIONS,
                           eye_shape_options=EYE_SHAPE_OPTIONS,
                           facial_features_options=FACIAL_FEATURES_OPTIONS,
                           eyebrows_options=EYEBROWS_OPTIONS,
                           nose_options=NOSE_OPTIONS,
                           mouth_options=MOUTH_OPTIONS,
                           clothing_style_options=CLOTHING_STYLE_OPTIONS,
                           personality_traits_options=PERSONALITY_TRAITS_OPTIONS,
                           pet_companion_options=PET_COMPANION_OPTIONS,
                           theme_options=THEME_OPTIONS,
                           format_options=FORMAT_OPTIONS)

def generate_story(characteristics, theme, format):
    story_prompt = f"Create a {format} story about a {theme} where the main character has the following characteristics: {characteristics}."
    
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=story_prompt,
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    story = response.choices[0].text.strip()
    return story

def generate_image_for_paragraph(paragraph):
    image_prompt = f"Generate an image for the following paragraph: {paragraph[:100]}"
    
    image_response = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size="1024x1024"
    )
    
    image_url = image_response['data'][0]['url']
    return image_url

@app.route('/generate', methods=['POST'])
def generate():
    # Collect form data
    gender = request.form['gender']
    age = request.form['age']
    skin_tone = request.form['skin_tone']
    hair_color = request.form['hair_color']
    hair_style = request.form['hair_style']
    eye_color = request.form['eye_color']
    eye_shape = request.form['eye_shape']
    facial_features = request.form['facial_features']
    eyebrows = request.form['eyebrows']
    nose = request.form['nose']
    mouth = request.form['mouth']
    clothing_style = request.form['clothing_style']
    personality_traits = request.form.get('personality_traits', '')
    pet_companion = request.form.get('pet_companion', '')

    characteristics = f"Gender: {gender}, Age: {age}, Skin Tone: {skin_tone}, Hair: {hair_color} {hair_style}, Eyes: {eye_color} {eye_shape}, Facial Features: {facial_features}, Eyebrows: {eyebrows}, Nose: {nose}, Mouth: {mouth}, Clothing Style: {clothing_style}"
    
    if personality_traits:
        characteristics += f", Personality Traits: {personality_traits}"
    if pet_companion:
        characteristics += f", Pet Companion: {pet_companion}"

    theme = request.form['theme']
    format = request.form['format']

    # Generate story and images
    story = generate_story(characteristics, theme, format)
    paragraphs = story.split('\n')
    images = []

    for paragraph in paragraphs[:5]:
      if paragraph.strip():
        image_url = generate_image_for_paragraph(paragraph)
        images.append(image_url)

    return jsonify({'story': paragraphs, 'images': images})

if __name__ == '__main__':
    app.run(debug=True)
