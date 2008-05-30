/******************************************************************************
 * QUANTA - A toolkit for High Performance Data Sharing
 * Copyright (C) 2003 Electronic Visualization Laboratory,  
 * University of Illinois at Chicago
 *
 * This library is free software; you can redistribute it and/or modify it 
 * under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either Version 2.1 of the License, or 
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public 
 * License for more details.
 * 
 * You should have received a copy of the GNU Lesser Public License along
 * with this library; if not, write to the Free Software Foundation, Inc., 
 * 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 *
 * Direct questions, comments etc about Quanta to cavern@evl.uic.edu
 *****************************************************************************/

#include <stdio.h>

#ifndef QUANTAMISC_HASHDICT_
#define QUANTAMISC_HASHDICT_

#include <stdlib.h>
#ifdef WIN32
#include <QUANTA/QUANTAconfig_win32.hxx>
#else /* !WIN32 */
#include <QUANTA/QUANTAconfig.hxx>
#endif /* WIN32 */
#include <QUANTA/QUANTAmisc_hash.hxx>
#include <QUANTA/md5Key_c.hxx>

#ifdef QUANTA_THREAD_SAFE
#include <QUANTA/QUANTAts_mutex_c.hxx>
#endif

#ifdef QUANTA_THREAD_SAFE
#define QUANTAMISC_HASHDICT_LOCK	mutex->lock();
#define QUANTAMISC_HASHDICT_UNLOCK mutex->unlock();
#endif

#ifdef NO_THREAD
#define QUANTAMISC_HASHDICT_LOCK
#define QUANTAMISC_HASHDICT_UNLOCK
#endif


template <class valueType, class keyType>
class QUANTAmisc_hashDict;

/*  A dictionary is stored as a collection of entries, each of which
 *  is an QUANTAmisc_hashDictEntry. It contains the key and value for the entry and
 *  a link to create lists of entries. 
 */
template <class valueType, class keyType>
class QUANTAmisc_hashDictEntry {

private:
	keyType		key;
	valueType		value;
	QUANTAmisc_hashDictEntry<valueType,keyType> *	next;

	QUANTAmisc_hashDictEntry(keyType k, valueType v)	{ key = k; value = v; };

	friend class QUANTAmisc_hashDict<valueType,keyType>;
};



/* QUANTAmisc_hashDict: a dictionary mapping (keyType) keys to 
 * (valueType) data pointers.
 * Whatever keyType is, it needs to have a type conversion mechanism to integer.
 * So if you are planning keyType to be some kind of object then that object's class
 * needs an operator int() converter in its class.
 */
template <class valueType, class keyType>
class QUANTAmisc_hashDict {

public:
	QUANTAmisc_hashDict(int entries = 1021);
	~QUANTAmisc_hashDict();


	// Manually lock this array object. (not recommended)
	void lock() {
		QUANTAMISC_HASHDICT_LOCK
	}

	// Manually unlock this array object. (not recommended)
	void unlock() {
		QUANTAMISC_HASHDICT_UNLOCK
	}

	// Calls given routine (passing value) for each entry in dictionary.
	//  The order of entries is not guaranteed to mean anything.
	// If routine returns 0 during an iteration the apply exits.
	// This can be used as an escape hatch.
	void applyToAll(int (*rtn)(keyType key, valueType value) );

	void showHashProfile();

	// This builds a linear array of entries out of the hash dictionary.
	// You must delete the list when done.
	valueType * buildListOfEntries(int *number);

	// Calls the given routine (passing value,data) for each entry in dictionary.
	//  The order of entries is not guaranteed to mean anything.
	// If routine returns 0 during an iteration the applyToAll exits. This can
	// be used as an escape hatch.
	// void *&retdata can be used to pass data into as well as out from the iteration.
	// Note that data passed in must first be type casted to void* to a separate
	// temporary ptr before the ptr is passed to the member function.
	// e.g. void *f;
	// f = (void*) data;
	// applyToAll(xxx,xxx,xxx,xxx, f);
	void applyToAll(int (*rtn)(keyType key, valueType value,
				   void *data1, void *data2, void *data3, void *&retdata),
			void *data1, void *data2, void *data3, void *&retdata );
	// Removes all entries from dictionary.
	void clear();

	/* Enters a key,value pair into the dictionary. Overwrites entry and
	 * returns FALSE if key already exists.
	 */
	int enter(keyType key, valueType value);

	/* Finds entry with given key, setting value to point to value.
	 * Returns FALSE if no such entry.
	 */
	int find(keyType key, valueType &value) const;

	// Removes the entry with the given key. Returns FALSE if no such entry
	int remove(keyType key);

	QUANTAmisc_hashDictEntry<valueType,keyType> *&findEntry(keyType key) const;

	int getNumItems(){return numberOfItems;}
private:

	int numberOfItems;

	// Entries in table
	int tableSize;

	// Entries are stored as an external hash table of QUANTAmisc_hashDictEntry instances.
	QUANTAmisc_hashDictEntry<valueType,keyType> **buckets;

#ifdef QUANTA_THREAD_SAFE
	QUANTAts_mutex_c *mutex;
#endif


};




template <class valueType, class keyType>
QUANTAmisc_hashDict<valueType,keyType>::QUANTAmisc_hashDict( int entries ) {

#ifdef QUANTA_THREAD_SAFE
		mutex = new QUANTAts_mutex_c;
#endif

	tableSize=entries;
	buckets=new QUANTAmisc_hashDictEntry<valueType,keyType> *[tableSize];
	for (int i = 0; i < tableSize; i++) {
		buckets[i] = NULL;
	}
	numberOfItems = 0;
}

template <class valueType, class keyType>
QUANTAmisc_hashDict<valueType,keyType>::~QUANTAmisc_hashDict() {
	clear();
	delete buckets;

#ifdef QUANTA_THREAD_SAFE
		delete mutex;
#endif

}

template <class valueType, class keyType>
void
QUANTAmisc_hashDict<valueType,keyType>::clear() {
	int i;
	QUANTAmisc_hashDictEntry<valueType,keyType> *entry, *nextEntry;
  
	for (i = 0; i < tableSize; i++) {
		for (entry = buckets[i]; entry != NULL; entry = nextEntry) {
			nextEntry = entry->next;
			delete entry;
		}
		buckets[i] = NULL;
	}
	numberOfItems = 0;
}




template <class valueType, class keyType>
int
QUANTAmisc_hashDict<valueType,keyType>::enter(keyType key, valueType value) {
QUANTAmisc_hashDictEntry<valueType,keyType>           *&entry = findEntry(key);
  
	if (entry == NULL) {
		entry = new QUANTAmisc_hashDictEntry<valueType,keyType>(key, value);
		entry->next = NULL;
		numberOfItems++;
		return 1;
	}
	else {
		entry->value = value;
		return 0;
	}
}

template <class valueType, class keyType>
int
QUANTAmisc_hashDict<valueType,keyType>::find(keyType key, valueType &value) const {

	QUANTAmisc_hashDictEntry<valueType,keyType>*&entry = findEntry(key);
  
	if (entry == NULL) {
		value = NULL;
		return 0;
	}
	else {
		value = entry->value;
		return 1;
	}
}

template <class valueType, class keyType>
QUANTAmisc_hashDictEntry<valueType,keyType> *&
QUANTAmisc_hashDict<valueType,keyType>::findEntry(keyType key) const {
	QUANTAmisc_hashDictEntry<valueType,keyType>           **entry;

	/*  
	int *keyFront = (int*) (key.key);

	int copyFront = *keyFront;

	// Make sure keyfront is positive.
	if (copyFront < 0) copyFront = -copyFront;
	*/

	int copyFront = key;

	entry = &buckets[copyFront % tableSize];

	while (*entry != NULL) {
		if ((*entry)->key == key) {
			break;
		}
		entry = &(*entry)->next;
	}
	return *entry;
}

template <class valueType, class keyType>
int
QUANTAmisc_hashDict<valueType,keyType>::remove(keyType key) {
	QUANTAmisc_hashDictEntry<valueType,keyType>           *&entry = findEntry(key);
	QUANTAmisc_hashDictEntry<valueType,keyType>           *tmp;
  
	if (entry == NULL) {
		return 0;
	}
	else {
		tmp = entry;
		entry = entry->next;
		delete tmp;
		numberOfItems--;
		return 1;
	}
}


template <class valueType, class keyType>
valueType*
QUANTAmisc_hashDict<valueType,keyType>::buildListOfEntries(int *number)
{
	int i;
	QUANTAmisc_hashDictEntry<valueType,keyType> *entry;

	valueType *list;

	int numItems = getNumItems();

	if (numItems == 0) {
		*number = 0;
		return NULL;
	}

	list = new valueType[numItems];
	if (list == NULL) {
		*number = 0;
		return NULL;
	}

	*number = numItems;

	int index = 0;

	// Call rtn for each entry in dict
	for (i = 0; i < tableSize; i++) {

		for (entry = buckets[i]; entry != NULL; entry = entry->next) {
			list[index] = entry->value;
			index++;
		}
	}
	return list;
}



// Calls given routine (passing value) for each entry in dictionary.
// The order of entries is not guaranteed to mean anything.
template <class valueType, class keyType>
void
QUANTAmisc_hashDict<valueType,keyType>::applyToAll(int (*rtn)(keyType key, valueType value) ) {
	int i;
	QUANTAmisc_hashDictEntry<valueType,keyType> *entry;

	// Call rtn for each entry in dict
	for (i = 0; i < tableSize; i++) {

		for (entry = buckets[i]; entry != NULL; entry = entry->next) {
			if (((*rtn)(entry->key, entry->value)) == 0) return;
		}
	}
}

template <class valueType, class keyType>
void QUANTAmisc_hashDict<valueType,keyType>::showHashProfile()
{
	int i, count;
	QUANTAmisc_hashDictEntry<valueType,keyType> *entry;

	// Call rtn for each entry in dict
	for (i = 0; i < tableSize; i++) {
		count = 0;
		for (entry = buckets[i]; entry != NULL; entry = entry->next) {
			count++;
		}
		if (count)
		printf("%04d: %d\n",i,count);
	}

}


// Calls given routine (passing value,data) for each entry in dictionary.
// The order of entries is not guaranteed to mean anything.
template <class valueType, class keyType>
void
QUANTAmisc_hashDict<valueType,keyType>::applyToAll(int (*rtn)(keyType key, valueType value,
							    void *data1, void *data2,
							    void *data3, void *&retdata),
						 void *data1, void *data2,
						 void *data3, void *&retdata) {
	int i;
	QUANTAmisc_hashDictEntry<valueType,keyType> *entry;

	// Call rtn for each entry in dict
	for (i = 0; i < tableSize; i++) {

		for (entry = buckets[i]; entry != NULL; entry = entry->next)
			if(((*rtn)(entry->key, entry->value, data1,data2,data3,retdata)) == 0) return;
	}
}


#endif // QUANTAMISC_HASHDICT_ 
