const KNOWLEDGE_BANK = {
    proverbs: [
        {
            id: 1,
            text: "Only a fool tests the depth of a river with both feet.",
            options: [
                { text: "It is good to swim in deep water.", value: 0.1 },
                { text: "Caution is the better part of valor.", value: 0.9 },
                { text: "Knowledge comes from experience.", value: 0.5 },
                { text: "Look before you leap.", value: 1.0 }
            ],
            truth: "Look before you leap."
        },
        {
            id: 2,
            text: "If you want to go fast, go alone. If you want to go far, go together.",
            options: [
                { text: "Speed is everything in life.", value: 0.2 },
                { text: "Community and collaboration ensure longevity.", value: 1.0 },
                { text: "Solitude brings focus.", value: 0.4 },
                { text: "Traveling is better in groups.", value: 0.7 }
            ],
            truth: "Community and collaboration ensure longevity."
        },
        {
            id: 3,
            text: "A bird that flies off the earth and lands on an anthill is still on the ground.",
            options: [
                { text: "Birds are meant to fly high.", value: 0.3 },
                { text: "Small changes do not change fundamental reality.", value: 1.0 },
                { text: "Every journey begins with a single step.", value: 0.5 },
                { text: "The earth is the source of all life.", value: 0.6 }
            ],
            truth: "Small changes do not change fundamental reality."
        },
        {
            id: 4,
            text: "Wisdom is like a baobab tree; no one individual can embrace it.",
            options: [
                { text: "Knowledge is vast and collective.", value: 1.0 },
                { text: "Baobab trees are very large.", value: 0.2 },
                { text: "Only elders have wisdom.", value: 0.4 },
                { text: "One should study nature to be wise.", value: 0.6 }
            ],
            truth: "Knowledge is vast and collective."
        },
        {
            id: 5,
            text: "The lizard that jumped from the high iroko tree said he would praise himself if no one else did.",
            options: [
                { text: "Lizards are great jumpers.", value: 0.1 },
                { text: "Self-worth and self-validation are essential.", value: 1.0 },
                { text: "Arrogance leads to a fall.", value: 0.3 },
                { text: "Always seek the praise of others.", value: 0.2 }
            ],
            truth: "Self-worth and self-validation are essential."
        },
        {
            id: 6,
            text: "A child who washes his hands properly will eat with elders.",
            options: [
                { text: "Hygiene is important for health.", value: 0.5 },
                { text: "Preparation and respect lead to opportunity.", value: 1.0 },
                { text: "Elders love clean children.", value: 0.3 },
                { text: "Hard work pays off.", value: 0.7 }
            ],
            truth: "Preparation and respect lead to opportunity."
        },
        {
            id: 7,
            text: "Until the lion has his own storyteller, the hunter will always have the best part of the story.",
            options: [
                { text: "Hunters are better at telling stories.", value: 0.2 },
                { text: "Perspective matters; one must tell their own story.", value: 1.0 },
                { text: "Lions cannot speak.", value: 0.1 },
                { text: "The truth is always objective.", value: 0.4 }
            ],
            truth: "Perspective matters; one must tell their own story."
        },
        {
            id: 8,
            text: "If the rhythm of the drum changes, the dance step must also change.",
            options: [
                { text: "Dancing is a form of expression.", value: 0.4 },
                { text: "Adaptability is key to survival and success.", value: 1.0 },
                { text: "Music dictates our actions.", value: 0.6 },
                { text: "Keep to the old ways no matter what.", value: 0.1 }
            ],
            truth: "Adaptability is key to survival and success."
        },
        {
            id: 9,
            text: "Smooth seas do not make skillful sailors.",
            options: [
                { text: "Sailing is a difficult profession.", value: 0.3 },
                { text: "Adversity and challenges build character and skill.", value: 1.0 },
                { text: "It is better to avoid storms.", value: 0.2 },
                { text: "Experience is the best teacher.", value: 0.7 }
            ],
            truth: "Adversity and challenges build character and skill."
        },
        {
            id: 10,
            text: "When an old man dies, a library burns to the ground.",
            options: [
                { text: "Elders are repositories of invaluable knowledge.", value: 1.0 },
                { text: "Books are more important than people.", value: 0.1 },
                { text: "Old age brings forgetfulness.", value: 0.2 },
                { text: "We should build more libraries.", value: 0.4 }
            ],
            truth: "Elders are repositories of invaluable knowledge."
        }
    ],
    riddles: [
        { id: 1, question: "I have a house that has no door.", answer: "An Egg" },
        { id: 2, question: "I have many eyes but cannot see.", answer: "A Pineapple" },
        { id: 3, question: "I drink from the earth but I never get full.", answer: "A Tree" },
        { id: 4, question: "I have no legs but I travel far.", answer: "A Voice" },
        { id: 5, question: "I am a king whose crown is always on.", answer: "A Rooster" },
        { id: 6, question: "I am small but I can carry a big man.", answer: "A Pair of Shoes" },
        { id: 7, question: "I have a thousand children but I am still a virgin.", answer: "A Tree with seeds" },
        { id: 8, question: "I have a mother but no father.", answer: "A River" },
        { id: 9, question: "I am a bridge that connects the living and the dead.", answer: "Memory" },
        { id: 10, question: "I am tall when I am young, and short when I am old.", answer: "A Candle" }
    ]
};
