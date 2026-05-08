"""
11 Veri Yapısı — Kamp Alanı Rezervasyon Sistemi
BMT210 Veri Yapıları — Gazi Üniversitesi 2026

1.  HashMap       — O(1) rezervasyon/ekipman erişimi
2.  BST           — Tarih bazlı sıralı sorgulama
3.  LinkedList    — Ziyaretçi geçmiş listesi
4.  Stack         — Son işlemi geri alma (LIFO)
5.  Queue         — Bekleme listesi (FIFO)
6.  PriorityQueue — VIP/Engelli öncelikli atama
7.  MaxHeap       — Popüler alan sıralaması
8.  CampSet       — Bakımdaki alanlar O(1) kontrol
9.  Graph         — Alan komşuluğu BFS/DFS
10. Matrix2D      — Alan tipi × gün doluluk matrisi
11. CampTree      — Kampın mekansal hiyerarşisi (N-ary ağaç)
"""


# ════════════════════════════════════════════════════
# 1. HASH MAP (Zincirleme / Chaining)
# ════════════════════════════════════════════════════

class _HNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashMap:
    """
    Zincirleme yöntemiyle çakışma çözen Hash Map.
    Kullanım: Rezervasyon/Ziyaretçi/Ekipman → O(1) erişim
    """

    def __init__(self, capacity=64):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        """O(1) ort. — ekle veya güncelle."""
        idx = self._hash(key)
        node = self.buckets[idx]
        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next
        new = _HNode(key, value)
        new.next = self.buckets[idx]
        self.buckets[idx] = new
        self.size += 1

    def get(self, key):
        """O(1) ort. — değer döndür, yoksa None."""
        idx = self._hash(key)
        node = self.buckets[idx]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def delete(self, key):
        """O(1) ort. — sil, başarı True/False."""
        idx = self._hash(key)
        node, prev = self.buckets[idx], None
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[idx] = node.next
                self.size -= 1
                return True
            prev, node = node, node.next
        return False

    def contains(self, key):
        return self.get(key) is not None

    def all_keys(self):
        keys = []
        for b in self.buckets:
            n = b
            while n:
                keys.append(n.key)
                n = n.next
        return keys

    def all_values(self):
        vals = []
        for b in self.buckets:
            n = b
            while n:
                vals.append(n.value)
                n = n.next
        return vals

    def __len__(self):
        return self.size

    def __repr__(self):
        return f"HashMap(size={self.size})"


# ════════════════════════════════════════════════════
# 2. BST — Binary Search Tree (İkili Arama Ağacı)
# ════════════════════════════════════════════════════

class _BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = self.right = None


class BST:
    """
    Tarih ve fiyat bazlı sıralı sorgulama.
    range_query(low, high) → [low, high] aralığındaki tüm kayıtlar.
    """

    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key, value):
        self.root = self._ins(self.root, key, value)

    def _ins(self, node, key, value):
        if node is None:
            self.size += 1
            return _BSTNode(key, value)
        if key < node.key:
            node.left = self._ins(node.left, key, value)
        elif key > node.key:
            node.right = self._ins(node.right, key, value)
        else:
            node.value = value
        return node

    def search(self, key):
        n = self.root
        while n:
            if key == n.key:
                return n.value
            n = n.left if key < n.key else n.right
        return None

    def range_query(self, low, high):
        """[low, high] dahil aralıkta tüm (key, value) çiftleri."""
        result = []
        self._range(self.root, low, high, result)
        return result

    def _range(self, node, low, high, result):
        if node is None:
            return
        if low < node.key:
            self._range(node.left, low, high, result)
        if low <= node.key <= high:
            result.append((node.key, node.value))
        if high > node.key:
            self._range(node.right, low, high, result)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)

    def delete(self, key):
        self.root, deleted = self._del(self.root, key)
        if deleted:
            self.size -= 1

    def _del(self, node, key):
        if node is None:
            return node, False
        deleted = False
        if key < node.key:
            node.left, deleted = self._del(node.left, key)
        elif key > node.key:
            node.right, deleted = self._del(node.right, key)
        else:
            deleted = True
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            m = node.right
            while m.left:
                m = m.left
            node.key, node.value = m.key, m.value
            node.right, _ = self._del(node.right, m.key)
        return node, deleted

    def __len__(self):
        return self.size


# ════════════════════════════════════════════════════
# 3. LINKED LIST (Çift Yönlü)
# ════════════════════════════════════════════════════

class _LLNode:
    def __init__(self, value):
        self.value = value
        self.prev = self.next = None


class LinkedList:
    """
    Ziyaretçi rezervasyon geçmişi.
    append / prepend / remove / iterate.
    """

    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def append(self, value):
        node = _LLNode(value)
        if self.tail:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        else:
            self.head = self.tail = node
        self.size += 1

    def prepend(self, value):
        node = _LLNode(value)
        if self.head:
            node.next = self.head
            self.head.prev = node
            self.head = node
        else:
            self.head = self.tail = node
        self.size += 1

    def remove(self, value):
        n = self.head
        while n:
            if n.value == value:
                if n.prev:
                    n.prev.next = n.next
                else:
                    self.head = n.next
                if n.next:
                    n.next.prev = n.prev
                else:
                    self.tail = n.prev
                self.size -= 1
                return True
            n = n.next
        return False

    def to_list(self):
        result, n = [], self.head
        while n:
            result.append(n.value)
            n = n.next
        return result

    def __len__(self):
        return self.size

    def __iter__(self):
        n = self.head
        while n:
            yield n.value
            n = n.next


# ════════════════════════════════════════════════════
# 4. STACK (LIFO — Son İşlemi Geri Al)
# ════════════════════════════════════════════════════

class Stack:
    """
    Geri alma (Undo) işlemi için.
    push / pop / peek — O(1)
    """

    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack boş")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)


# ════════════════════════════════════════════════════
# 5. QUEUE (FIFO — Bekleme Listesi)
# ════════════════════════════════════════════════════

from collections import deque


class Queue:
    """
    Rezervasyon bekleme kuyruğu.
    enqueue / dequeue — O(1)
    """

    def __init__(self):
        self._data = deque()

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Kuyruk boş")
        return self._data.popleft()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def to_list(self):
        return list(self._data)

    def __len__(self):
        return len(self._data)


# ════════════════════════════════════════════════════
# 6. PRIORITY QUEUE (VIP / Engelli Önceliği)
# ════════════════════════════════════════════════════

import heapq


class PriorityQueue:
    """
    Öncelik sırasına göre alan atama.
    Yüksek öncelik önce çıkar (max-heap simülasyonu).
    """

    def __init__(self):
        self._heap = []
        self._counter = 0   # eşit öncelik için bozucu

    def enqueue(self, item, priority):
        # Python min-heap → negatif ile max-heap
        heapq.heappush(self._heap, (-priority, self._counter, item))
        self._counter += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("PQ boş")
        _, _, item = heapq.heappop(self._heap)
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self._heap[0][2]

    def is_empty(self):
        return len(self._heap) == 0

    def to_list(self):
        # Return items sorted by priority (highest first)
        return [item for _, _, item in sorted(self._heap)]

    def remove_item(self, item):
        # Remove a specific item from the queue
        for i, (_, _, it) in enumerate(self._heap):
            if it == item:
                del self._heap[i]
                heapq.heapify(self._heap)
                return True
        return False

    def __len__(self):
        return len(self._heap)


# ════════════════════════════════════════════════════
# 7. MAX HEAP (Popüler Alan Sıralaması)
# ════════════════════════════════════════════════════

class MaxHeap:
    """
    Rezervasyon sayısına göre en popüler alanları bulur.
    top_k(k) → en çok rezervasyon yapılan k alan.
    """

    def __init__(self):
        self._data = []   # (değer, nesne) — negatif ile max

    def push(self, value, item):
        heapq.heappush(self._data, (-value, item))

    def pop(self):
        if not self._data:
            raise IndexError("Heap boş")
        neg, item = heapq.heappop(self._data)
        return -neg, item

    def top_k(self, k):
        """En büyük k elemanı döndürür (heap bozulmaz)."""
        snapshot = list(self._data)
        result = []
        for _ in range(min(k, len(snapshot))):
            if not snapshot:
                break
            neg, item = heapq.heappop(snapshot)
            result.append((-neg, item))
        return result

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)


# ════════════════════════════════════════════════════
# 8. CAMP SET (Bakımdaki Alanlar — O(1) Kontrol)
# ════════════════════════════════════════════════════

class CampSet:
    """
    Bakımdaki alan ID'lerini tutar.
    add / remove / contains — O(1)
    """

    def __init__(self):
        self._data = set()

    def add(self, alan_id):
        self._data.add(alan_id)

    def remove(self, alan_id):
        self._data.discard(alan_id)

    def contains(self, alan_id):
        return alan_id in self._data

    def all(self):
        return list(self._data)

    def __len__(self):
        return len(self._data)


# ════════════════════════════════════════════════════
# 9. GRAPH (Alan Komşuluğu — BFS / DFS)
# ════════════════════════════════════════════════════

class Graph:
    """
    Kampın alanları arasındaki komşuluk ilişkisi.
    bfs(start) / dfs(start) → erişilebilen alan listesi.
    """

    def __init__(self):
        self._adj = {}   # alan_id → {komşu_id: mesafe}

    def add_node(self, node_id):
        if node_id not in self._adj:
            self._adj[node_id] = {}

    def add_edge(self, u, v, weight=1):
        self.add_node(u)
        self.add_node(v)
        self._adj[u][v] = weight
        self._adj[v][u] = weight

    def remove_node(self, node_id):
        if node_id in self._adj:
            for neighbor in list(self._adj[node_id]):
                self._adj[neighbor].pop(node_id, None)
            del self._adj[node_id]

    def neighbors(self, node_id):
        return list(self._adj.get(node_id, {}).keys())

    def bfs(self, start):
        """Genişlik öncelikli arama — erişim sırası listesi."""
        if start not in self._adj:
            return []
        visited, queue, result = {start}, deque([start]), []
        while queue:
            node = queue.popleft()
            result.append(node)
            for nb in self._adj[node]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        return result

    def dfs(self, start):
        """Derinlik öncelikli arama — erişim sırası listesi."""
        if start not in self._adj:
            return []
        visited, result = set(), []

        def _dfs(node):
            visited.add(node)
            result.append(node)
            for nb in self._adj[node]:
                if nb not in visited:
                    _dfs(nb)

        _dfs(start)
        return result

    def all_nodes(self):
        return list(self._adj.keys())

    def dijkstra(self, start, end):
        """Dijkstra En Kısa Yol Algoritması. 
        Döndürür: (mesafe, yol_listesi)"""
        import heapq
        if start not in self._adj or end not in self._adj:
            return float('inf'), []

        distances = {node: float('inf') for node in self._adj}
        distances[start] = 0
        previous = {node: None for node in self._adj}
        
        pq = [(0, start)]
        
        while pq:
            current_dist, current_node = heapq.heappop(pq)
            
            if current_node == end:
                break
                
            if current_dist > distances[current_node]:
                continue
                
            for neighbor, weight in self._adj[current_node].items():
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
                    
        path = []
        curr = end
        while curr is not None:
            path.insert(0, curr)
            curr = previous[curr]
            
        if distances[end] == float('inf'):
            return float('inf'), []
            
        return distances[end], path

    def __len__(self):
        return len(self._adj)


# ════════════════════════════════════════════════════
# 10. MATRIX 2D (Alan Tipi × Gün Doluluk Matrisi)
# ════════════════════════════════════════════════════

class Matrix2D:
    """
    Satır: alan tipleri (Çadır, Karavan, Bungalov)
    Sütun: haftanın günleri (0=Pzt … 6=Paz)
    Değer: o gün o tipteki rezervasyon sayısı.
    """

    def __init__(self, rows, cols, default=0):
        self.rows = rows
        self.cols = cols
        self._data = [[default] * cols for _ in range(rows)]

    def set(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self._data[row][col] = value

    def get(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self._data[row][col]
        return None

    def increment(self, row, col, amount=1):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self._data[row][col] += amount

    def row_sum(self, row):
        return sum(self._data[row])

    def col_sum(self, col):
        return sum(self._data[r][col] for r in range(self.rows))

    def to_list(self):
        return [row[:] for row in self._data]

    def __repr__(self):
        lines = [f"Matrix2D({self.rows}×{self.cols}):"]
        for row in self._data:
            lines.append("  " + str(row))
        return "\n".join(lines)


# ════════════════════════════════════════════════════
# 11. CAMP TREE — Mekansal Hiyerarşi (N-ary Ağaç)
# ════════════════════════════════════════════════════

class _TreeNode:
    """N-ary ağaç düğümü."""
    def __init__(self, name, alan_id=None):
        self.name = name          # Görünen ad (bölge veya alan_id)
        self.alan_id = alan_id    # Yalnızca yaprak düğümlerde dolu
        self.children = []        # Alt düğümler
        self.parent = None        # Üst düğüm (root için None)

    @property
    def is_leaf(self):
        return self.alan_id is not None


class CampTree:
    """
    Kampın mekansal hiyerarşisini tutan N-ary ağaç.

    Yapı:
        Kök          → "Kamp Ana Girişi"
        Dal (x3)     → "Çadır Bölgesi" | "Karavan Bölgesi" | "Bungalov Bölgesi"
        Yaprak       → Alan ID (A0001, A0002 …)

    Kullanım:
        - alan_ekle(alan_id, alan_tipi)  → doğru bölgeye yerleştirir
        - alan_sil(alan_id)              → yaprağı kaldırır
        - bolge_alanlari(alan_tipi)      → bölgedeki tüm alan ID'leri
        - tum_bolgeler()                 → {bölge: [alan_id, ...]} sözlüğü
        - hiyerarsi_yazdir()             → raporlama için metin ağacı
        - bfs() / dfs()                  → ağaç gezimi
        - alan_bolgesi(alan_id)          → hangi bölgede olduğunu söyler
    """

    # Alan tipini bölge adına eşleyen sabit sözlük
    BOLGE_MAP = {
        "Çadır":   "Çadır Bölgesi",
        "Karavan": "Karavan Bölgesi",
        "Bungalov": "Bungalov Bölgesi",
    }

    def __init__(self):
        self.root = _TreeNode("Kamp Ana Girişi")

        # Üç sabit dal oluştur
        self._bolge_nodes: dict[str, _TreeNode] = {}
        for bolge_adi in ["Çadır Bölgesi", "Karavan Bölgesi", "Bungalov Bölgesi"]:
            node = _TreeNode(bolge_adi)
            node.parent = self.root
            self.root.children.append(node)
            self._bolge_nodes[bolge_adi] = node

        # alan_id → yaprak düğüm (O(1) erişim)
        self._alan_nodes: dict[str, _TreeNode] = {}

    # ── Ekleme / Silme ──────────────────────────────

    def alan_ekle(self, alan_id: str, alan_tipi: str) -> bool:
        """
        Verilen alan_id'yi alan_tipi'ne göre uygun bölgeye yaprak olarak ekler.
        Bilinmeyen tipler varsayılan olarak "Çadır Bölgesi"ne gider.
        Aynı alan_id ikinci kez eklenemez → False döner.
        """
        if alan_id in self._alan_nodes:
            return False
        bolge_adi = self.BOLGE_MAP.get(alan_tipi, "Çadır Bölgesi")
        bolge_node = self._bolge_nodes[bolge_adi]
        yaprak = _TreeNode(alan_id, alan_id=alan_id)
        yaprak.parent = bolge_node
        bolge_node.children.append(yaprak)
        self._alan_nodes[alan_id] = yaprak
        return True

    def alan_sil(self, alan_id: str) -> bool:
        """
        Yaprağı ağaçtan kaldırır.  Bölge düğümleri etkilenmez.
        Bulunamazsa False döner.
        """
        node = self._alan_nodes.get(alan_id)
        if node is None:
            return False
        if node.parent:
            node.parent.children.remove(node)
        del self._alan_nodes[alan_id]
        return True

    # ── Sorgulama ───────────────────────────────────

    def bolge_alanlari(self, alan_tipi: str) -> list:
        """Belirli bir alan tipine ait tüm alan ID'lerini döndürür."""
        bolge_adi = self.BOLGE_MAP.get(alan_tipi, alan_tipi)
        bolge_node = self._bolge_nodes.get(bolge_adi)
        if bolge_node is None:
            return []
        return [c.alan_id for c in bolge_node.children if c.is_leaf]

    def tum_bolgeler(self) -> dict:
        """
        Her bölgenin alan listesini döndürür.
        {bölge_adı: [alan_id, ...]}
        """
        return {
            adi: [c.alan_id for c in node.children if c.is_leaf]
            for adi, node in self._bolge_nodes.items()
        }

    def alan_bolgesi(self, alan_id: str):
        """Alan ID'sinin bağlı olduğu bölge adını döndürür; bulunamazsa None."""
        node = self._alan_nodes.get(alan_id)
        if node and node.parent:
            return node.parent.name
        return None

    def bolge_alan_sayisi(self, alan_tipi: str) -> int:
        """Bir bölgedeki alan sayısını döndürür."""
        return len(self.bolge_alanlari(alan_tipi))

    def icerir(self, alan_id: str) -> bool:
        """Alan ID'sinin ağaçta olup olmadığını kontrol eder — O(1)."""
        return alan_id in self._alan_nodes

    # ── Gezim ───────────────────────────────────────

    def bfs(self) -> list:
        """
        Genişlik öncelikli ağaç gezimi.
        Döndürür: [(seviye, düğüm_adı), ...]
        """
        from collections import deque
        result = []
        q = deque([(self.root, 0)])
        while q:
            node, lvl = q.popleft()
            result.append((lvl, node.name))
            for child in node.children:
                q.append((child, lvl + 1))
        return result

    def dfs(self, node=None, seviye=0) -> list:
        """
        Derinlik öncelikli önyüz (pre-order) gezimi.
        Döndürür: [(seviye, düğüm_adı), ...]
        """
        if node is None:
            node = self.root
        result = [(seviye, node.name)]
        for child in node.children:
            result.extend(self.dfs(child, seviye + 1))
        return result

    # ── Raporlama ───────────────────────────────────

    def hiyerarsi_yazdir(self) -> list:
        """
        Ağaç hiyerarşisini metin satırları listesi olarak döndürür.
        Örnek çıktı:
            🏕️  Kamp Ana Girişi
            ├── 🏕  Çadır Bölgesi  (2 parsel)
            │    ├── A001
            │    └── A002
            ├── 🚐  Karavan Bölgesi  (1 parsel)
            │    └── A003
            └── ⛺  Bungalov Bölgesi  (0 parsel)
        """
        IKONLAR = {
            "Kamp Ana Girişi": "🏕️",
            "Çadır Bölgesi":   "⛺",
            "Karavan Bölgesi": "🚐",
            "Bungalov Bölgesi":"🏕",
        }
        lines = []

        def _yaz(node, prefix="", is_last=True):
            baglanti = "└── " if is_last else "├── "
            ikon = IKONLAR.get(node.name, "📍")
            if node.parent is None:
                # Kök
                ek_bilgi = f"  ({len(self._alan_nodes)} toplam parsel)"
                lines.append(f"{ikon}  {node.name}{ek_bilgi}")
            else:
                if not node.is_leaf:
                    ek_bilgi = f"  ({len(node.children)} parsel)"
                    lines.append(f"{prefix}{baglanti}{ikon} {node.name}{ek_bilgi}")
                else:
                    lines.append(f"{prefix}{baglanti}{ikon} {node.name}")

            child_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                _yaz(child, child_prefix, i == len(node.children) - 1)

        _yaz(self.root)
        return lines

    # ── Dunder ──────────────────────────────────────

    def __len__(self):
        """Ağaçtaki toplam yaprak (alan) sayısı."""
        return len(self._alan_nodes)

    def __repr__(self):
        bolge_ozet = ", ".join(
            f"{adi}:{len(node.children)}"
            for adi, node in self._bolge_nodes.items()
        )
        return f"CampTree(toplam={len(self)}, [{bolge_ozet}])"