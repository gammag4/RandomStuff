
# serialization
bincode
serde

# async/threaded/mpmc communication
tokio
tokio_stream
futures_util
rayon
crossbeam-channel
async_channel

# logging/monitoring
tracing
prometheus

# communications
socket2
quinn
rustls
hickory_resolver # custom dns resolver (does not use system dns resolver)

rand # random
lz_fear # lz compression
async_trait # type erasure for async
byteorder # big-endian/little-endian order
bytes # byte slices manipulation
hashbrown # really efficient hashmap impl
image # image enc/dec
num # number types


specs
bevy # apparently has both table and sparseset structures
shipyard # uses SparseSet structure



tokio tut: https://tokio.rs/tokio/tutorial
tokio + rayon: https://ryhl.io/blog/async-what-is-blocking/#the-rayon-crate
demistifying async await: https://ruspiro.github.io/ruspiro-async-book/cover.html

make code in bevy then benchmark it using both table and sparseset implementations
