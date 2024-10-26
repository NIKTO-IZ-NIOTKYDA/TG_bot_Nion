import React, { useState, useEffect } from 'react';

function changeLetterCase(str, index) {
    if (index < 0 || index >= str.length) {
        console.error("Индекс вне диапазона!");
        return str; // вернем оригинальную строку, если индекс вне диапазона
    }

    const before = str.slice(0, index);
    const letter = str[index];
    const after = str.slice(index + 1);

    const newLetter = letter === letter.toUpperCase() ? letter.toLowerCase() : letter.toUpperCase();

    return before + newLetter + after;
}

export const TextAnimator = (props) => {
    const originalText = props.text;
    const [index, setIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setIndex(prevIndex => {
                // Проверяем, нужно ли сбросить индекс
                if (prevIndex < originalText.length - 1) {
                    return prevIndex + 1;
                } else {
                    return 0; // Сбросим индекс на 0, чтобы начать сначала
                }
            });
        }, 150);

        // Очищаем интервал при размонтировании
        return () => clearInterval(interval);
    }, [originalText.length]); // Следим за длиной текста

    return changeLetterCase(originalText, index);
};

export default TextAnimator;
