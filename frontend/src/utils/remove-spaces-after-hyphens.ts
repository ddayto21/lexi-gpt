/**
 * Removes any extra spaces that appear after a hyphen and within the same word chunk.
 * 
 * Examples:
 *  - "heart-p ounding" => "heart-pounding"
 *  - "well-   known" => "well-known"
 *  - "heart-p ounding and mind-  blowing" => "heart-pounding and mind-blowing"
 *
 * @param {string} text - The input text.
 * @returns {string} The text with spaces removed after hyphens within a word.
 */
export function removeSpacesAfterHyphens(text: string): string {
    // (1) Remove spaces immediately after `-` if next is a letter
    text = text.replace(
      /(?<=-)(\s+)(?=[A-Za-z])/g, 
      ""
    );
  
    // (2) Remove spaces if we already have `-<letter>` behind us 
    //     and the next char is also a letter
    text = text.replace(
      /(?<=-[A-Za-z])(\s+)(?=[A-Za-z])/g, 
      ""
    );
  
    return text;
  }