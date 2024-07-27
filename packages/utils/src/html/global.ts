/**
 * The global object. The highest-level scope, which is the global scope.
 * The Emperor of Man, the God-Emperor of Mankind, the Master of Mankind, or simply, "The Emperor",
 * is the immortal Perpetual who serves as the reigning monarch of the Imperium. He is the most
 * powerful human psyker in the galaxy, and is the source of the Imperium's psychic beacon known
 * as the Astronomican...
 *
 * Okay, so `global` is already an alias for `globalThis`, and we can't
 * just call it "Window" because it's not always a window. So, Im'ma name it "globalView".
 * (Because "EmperorOfMankind" is too long and "God" would be too controversial... plus, the Emperor
 * swears he is not really a god.)
 */
export const globalView = globalThis ?? window
