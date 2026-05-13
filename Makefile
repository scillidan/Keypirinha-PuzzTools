PACKAGE_NAME = PuzzTools
VERSION = 0.0.1
DIST_DIR = dist
FILES = puzz_tools.py transforms.py README.md CHANGELOG.md LICENSE

.PHONY: all clean dist

all: dist

dist:
	@mkdir -p $(DIST_DIR)
	7z a -tzip "$(DIST_DIR)/$(PACKAGE_NAME).keypirinha-package" $(FILES)

clean:
	@rm -rf $(DIST_DIR)

info:
	@echo "Package: $(PACKAGE_NAME)"
	@echo "Version: $(VERSION)"
	@echo "Files: $(FILES)"
