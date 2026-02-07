# Audio I2S & Codecs

Zephyr's **I2S (Inter-IC Sound)** API handles digital audio data transfer. It is typically paired with an external Audio Codec driver for DAC/ADC conversion.

## Core Concepts
- **Data Format**: I2S, Left Justified, Right Justified.
- **Channels**: Typically Stereo (Left/Right) or Mono.
- **Sampling Rate**: 44.1kHz, 48kHz, etc.
- **Word Size**: 16-bit, 24-bit, or 32-bit.

## Configuration
```kconfig
CONFIG_I2S=y
CONFIG_AUDIO=y      # High-level audio subsystem
CONFIG_AUDIO_CODEC=y
```

## Implementation Patterns

### 1. Initializing I2S
```c
#include <zephyr/drivers/i2s.h>

void init_audio(void) {
    const struct device *i2s_dev = DEVICE_DT_GET(DT_NODELABEL(i2s0));
    struct i2s_config config = {
        .word_size = 16,
        .channels = 2,
        .format = I2S_FMT_DATA_FORMAT_I2S,
        .options = I2S_OPT_FRAME_CLK_SLAVE | I2S_OPT_BIT_CLK_SLAVE,
        .frame_clk_freq = 44100,
        .mem_slab = &audio_slab,
        .timeout = 1000,
    };
    
    i2s_configure(i2s_dev, I2S_DIR_TX, &config);
}
```

### 2. Streaming Audio
Use memory slabs to manage a queue of audio buffers that are sent to the I2S peripheral via DMA.

```c
void play_buffer(void *data, size_t len) {
    void *mem_ptr;
    k_mem_slab_alloc(&audio_slab, &mem_ptr, K_NO_WAIT);
    memcpy(mem_ptr, data, len);
    i2s_write(i2s_dev, mem_ptr, len);
}
```

## Professional Strategies
- **Ping-Pong Buffering**: Always use at least two buffers to ensure the I2S DMA always has data ready while the application is filling the next buffer. See **[hardware-io](../../hardware-io/SKILL.md)** for DMA configuration patterns.
- **Volume Ramping**: Gradually increase/decrease volume in software to prevent "pops" and "clicks" when starting or stopping audio.
- **Devicetree**: Link your I2S device to the corresponding Audio Codec using the `codec` property in DT.
