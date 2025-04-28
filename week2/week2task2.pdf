import random  # Import the random module to simulate random events

# Function to feed the pet
# This function decreases the pet's hunger and reduces happiness slightly when feeding.
def feed_pet(pet):
    print(f"You feed {pet['name']}...")
    pet['hunger'] = max(0, pet['hunger'] - 20)  # Decrease hunger, but ensure it doesn't go below 0
    pet['happiness'] = max(0, pet['happiness'] - 5)  # Decrease happiness, but ensure it doesn't go below 0
    print(f"{pet['name']} looks satisfied!\n")

# Function to play with the pet
# This function increases the pet's happiness and also slightly increases its hunger.
def play_with_pet(pet):
    print(f"You play with {pet['name']}...")
    pet['happiness'] = min(100, pet['happiness'] + 20)  # Increase happiness, but ensure it doesn't exceed 100
    pet['hunger'] = min(100, pet['hunger'] + 5)  # Increase hunger, but ensure it doesn't exceed 100
    print(f"{pet['name']} is having a lot of fun!\n")

# Function to check the pet's current hunger and happiness levels
# This function prints the pet's current status for both hunger and happiness.
def check_status(pet):
    print(f"\n{pet['name']}'s Status:")
    print(f"Hunger: {pet['hunger']}")
    print(f"Happiness: {pet['happiness']}\n")

# Function to simulate the passage of time
# Over time, hunger increases slightly, and happiness decreases slightly.
def time_passes(pet):
    pet['hunger'] = min(100, pet['hunger'] + 5)  # Hunger increases over time, but doesn't exceed 100
    pet['happiness'] = max(0, pet['happiness'] - 5)  # Happiness decreases over time, but doesn't go below 0

# Function to handle random events
# This function randomly triggers one of three events: finding a snack, getting sick, or nothing.
def random_event(pet):
    event = random.choice(['snack', 'sick', 'nothing'])  # Randomly choose an event
    if event == 'snack':
        print(f"\n{pet['name']} found a snack! Hunger decreases.")
        pet['hunger'] = max(0, pet['hunger'] - 10)  # Decrease hunger, but ensure it doesn't go below 0
    elif event == 'sick':
        print(f"\nOh no! {pet['name']} feels sick. Happiness decreases.")
        pet['happiness'] = max(0, pet['happiness'] - 15)  # Decrease happiness, but ensure it doesn't go below 0
    # If 'nothing' is chosen, no change occurs

# Main function that controls the overall game flow
# The function handles user input, makes the pet interact with actions, and checks for game-ending conditions.
def main():
    print("Welcome to the Virtual Pet Simulator!")
    pet_name = input("What would you like to name your pet? ")  # Ask the player for the pet's name
    
    pet = {  # Initialize the pet's starting attributes
        'name': pet_name,
        'hunger': 50,  # Initial hunger level
        'happiness': 50  # Initial happiness level
    }
    
    action_count = 0  # Counter to track the number of actions the player has taken
    
    while True:  # Main game loop
        print("\nWhat would you like to do?")
        print("1. Feed your pet")
        print("2. Play with your pet")
        print("3. Check your pet's status")
        print("4. Quit")
        
        choice = input("Enter your choice (1-4): ")  # Get player input for action
        
        if choice == '1':
            feed_pet(pet)  # Call feed_pet function if player chooses to feed the pet
        elif choice == '2':
            play_with_pet(pet)  # Call play_with_pet function if player chooses to play with the pet
        elif choice == '3':
            check_status(pet)  # Call check_status function to show the pet's current state
        elif choice == '4':
            print(f"Goodbye! {pet['name']} will miss you!")  # End the game if player chooses to quit
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")  # Handle invalid input
            continue
        
        action_count += 1  # Increment the action count after each choice
        
        if action_count % 2 == 0:  # Every 2 actions, simulate the passage of time and check for random events
            time_passes(pet)
            random_event(pet)
        
        if pet['hunger'] > 80:  # Check if the pet is very hungry (above 80)
            pet['happiness'] = max(0, pet['happiness'] - 10)  # Decrease happiness if the pet is too hungry
            print(f"\n{pet['name']} is very hungry and looks sad.")
        
        if pet['hunger'] >= 100:  # End the game if the pet's hunger reaches 100
            print(f"\n{pet['name']} became too hungry... Game Over!")
            break
        if pet['happiness'] <= 0:  # End the game if the pet's happiness reaches 0
            print(f"\n{pet['name']} became too sad... Game Over!")
            break

if __name__ == "__main__":
    main()  # Start the game
